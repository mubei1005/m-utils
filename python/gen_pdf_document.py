# coding:utf-8
import os
import time

from reportlab.lib.styles import getSampleStyleSheet     # 样式库
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Image
from reportlab.pdfbase import pdfmetrics                 # 字体注册
from reportlab.pdfbase.ttfonts import TTFont             # 字体
from reportlab.lib.units import cm                       # 尺寸
from reportlab.lib import colors                         # 颜色
from reportlab.lib.pagesizes import A4                   # 页面尺寸
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle

# 字体注册，注册两种字体为了方便不同形式的内容展示
# 注意字体文件(ttf文件）一定要存在

pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))
# pdfmetrics.registerFont(TTFont('fs', 'fs.ttf'))

# 页眉页脚样式
def headerFooterStyle(alignment=2):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = "simsun"
    styleN.fontSize = 10
    styleN.textColor = colors.gray
    
    styleN.spaceBefore = 30         # 段前间距
    styleN.alignment = alignment    # 居中

    return styleN

# 标题样式
def titleStyle():
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = "simsun"    # 字体
    styleN.fontSize = 28          # 字体大小
    styleN.alignment = 1          # 居中，居左为0
    #styleN.leading = 80          # 行距
    styleN.spaceBefore = 10       # 段前间距
    styleN.spaceAfter = 20        # 段后间距

    return styleN

# 正文样式
def textStyle(fontSize=12, lineIndent=0, alignment=0):
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = "simsun"
    styleN.fontSize = fontSize
    
    styleN.alignment = alignment        # 居中，居左为0
    styleN.leading = 24                 # 行距
    styleN.firstLineIndent = lineIndent #首行缩进2个字(fontSize的2倍)
    return styleN

# 页眉
def header(canvas, doc):
    canvas.saveState()
    p = Paragraph("检测报告", headerFooterStyle())
    w,h = p.wrap(doc.width, doc.topMargin)
    p.drawOn(canvas, doc.leftMargin, doc.bottomMargin+ doc.height + 1*cm)
    canvas.setStrokeColor(colors.gray)
    #画线（页眉底部的横线）
    canvas.line(doc.leftMargin, doc.bottomMargin+doc.height + 0.5*cm, doc.leftMargin+doc.width, doc.bottomMargin+doc.height + 0.5*cm)
    canvas.restoreState()
    
# 页脚（这里页脚只有页码）
def footer(canvas, doc):
    canvas.saveState()
    pageNumber = ("%s" %canvas.getPageNumber())
    p = Paragraph(pageNumber, headerFooterStyle(1))
    w, h = p.wrap(doc.width, doc.bottomMargin)

    # -1cm 的目的是为了让页码在2cm的下边距里上下居中
    p.drawOn(canvas,doc.leftMargin,doc.bottomMargin-1*cm)
    canvas.restoreState()

# if __name__ == '__main__':
#     cachename = 'cache.txt'
def gen_pdf_document(cachename = 'cache/cache.txt'):
    # cache.txt 文件格式如下：
    '''
    titl: XXX大桥检测报告
    text: 桥梁描述: 真皮网关网购润王朝切割闹
    itxt: 桥梁整体图片
    imag: crack_00003.jpg
    itxt: 桥梁具体图片
    imag: crack_00003.jpg
    text: 桥梁检测情况: 真皮网关网购润王朝切割闹
    '''
    # cache.txt 文件内容说明：
	# cache.txt 文件的内容为有序系列， 第一行一般应该设置为 titl， 生成的PDF 内容顺序与此文件内容顺序相同
	# 支持文本 及 图片 两种类容
    '''
	titl  ——  表示项目名称,一般唯一一行， 如果有多个 titl 标签，则取第一个
	text  ——  表示段落文本内容，自动换行， 一行表示一个段落
	itxt  ——  表示图片描述文本（行居中， 在图片上方，itxt 的下一行必须对应描述的图片路径，由imag表示）
	imag  ——  表示图片路径（相对路径和绝对路径均可， 独立出现或则在itxt的下一行出现）
    
    '''
    
    if not os.path.exists(cachename):
	    print("cache file " + cachename + "not exists...")
        return 0
	
    #正文（从文本文件中读取一段文字）
    fcache = open(cachename, 'r', encoding='UTF-8')
    fcache_text = fcache.read()
    fcache.close()
    fcache_line = fcache_text.split("\n")
        
    for pline in fcache_line:
        ptype = pline.strip()[:4]
        if ptype == "titl":
           ptitle = pline[5:].strip()
           break
        else:
           ptitle = "桥梁检测报告"
    cache_path = 'cache/'
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    report_file = cache_path + ptitle + ".pdf"
    # 文档属性，保存路径，页面大小和页边距
    doc = BaseDocTemplate(report_file, pagesize = A4,topMargin = 2*cm, bottomMargin = 2*cm)
    # 内容区域
    frame= Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    # 页面模板
    template = PageTemplate(id='e11', frames=frame, onPage=header, onPageEnd=footer)
    doc.addPageTemplates([template])

    # 文档标题
    title = Paragraph("检测报告", titleStyle())
    blankline = Paragraph("\0", textStyle())

    content = []
    
    # 添加空白行
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    
    # 文档标题行
    content.append(title)
    
    # 添加空白行
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    content.append(blankline)
    
    projectname = "检测项目： " + ptitle
    projectline = Paragraph(projectname, textStyle(15, 80))
    
    content.append(projectline)
    
    reportdate = "报告日期： " + time.strftime("%Y 年 %m 月 %d 日")
    reportdateline = Paragraph(reportdate, textStyle(15, 80))
    
    content.append(reportdateline)
    
    # 分页， 把文档封面标题等信息与文档内（正文分开）
    content.append(PageBreak())
       
    for pline in fcache_line:
        ptype = pline.strip()[:4]
        if ptype == "text":
            text = Paragraph(pline[5:].strip(), textStyle())
            content.append(text)
        elif ptype == "itxt":
            text = Paragraph(pline[5:].strip(), textStyle(alignment=1))
            content.append(text)
        elif ptype == "imag":
            # 添加图片
            img = Image(pline[5:].strip())
            img.drawWidth = doc.width
            # img.drawHeight = 200
            content.append(img)
            content.append(blankline)
    
    doc.build(content)
	
    pdf_name = os.path.dirname(os.path.abspath(__file__)) + '/' + report_file
    # print(pdf_name)
    os.system("start " + pdf_name)
    return 0 

# pip install reportlab==4.0.4
# 调用示例

if __name__ == '__main__':
    #正文（从文本文件中读取一段文字）
    gen_pdf_document()
#    gen_pdf_document('template/cache1.txt')



