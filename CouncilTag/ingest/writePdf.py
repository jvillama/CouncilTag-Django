from PyPDF2 import PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from CouncilTag.ingest.models import Message, Committee 
from CouncilTag.api.utils import send_mail
import io
from datetime import datetime, date
import os



def paragraphize_comments(comments, contents):
    ps_email = ParagraphStyle(
        "Email", fontSize=10, leftIndent=0.25 * inch, textColor="#000000")
    ps_name = ParagraphStyle(
        "name", fontSize=10, leftIndent=0.25 * inch, spaceBefore=10, textColor="#000000")
    ps_comment = ParagraphStyle(
        "Comment", fontSize=10, leftIndent=0.25 * inch, textColor="#000000")
    for comment in comments:
        if comment.email is not None:
            name = "Name: " + comment.first_name + " " + comment.last_name
            email = "Email: <a href='mailto:" + str(comment.user.email) + "'>" + comment.user.email + "</a>"
            comment = "Comment: " + comment.content
        elif comment.user is not None:
            name = "Name: " + comment.first_name + " " + comment.last_name
            email = "Email: <a href='mailto:" + str(comment.user.email) + "'>" + comment.user.email + "</a>"
            comment = "Comment: " + comment.content
        else:
            continue
        contents.append(Paragraph(name, ps_name))
        contents.append(Paragraph(email, ps_email))
        contents.append(Paragraph(comment, ps_comment))
    return contents


def writePdfForAgendaItems(agenda_items):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    static = 'PDF_Reports'
    full_path = os.path.join(root_dir,static)
    today = datetime.today()

    if not os.path.exists(full_path):
        os.mkdir(full_path)

    try:
        doc = SimpleDocTemplate(str(full_path) + "/Meeting_" + str(datetime.fromtimestamp(agenda_items[0].agenda.meeting_time).strftime('%Y%m%d')) + ".pdf",
                                pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        contents = []

        # Paragraph styles
        ps_title = ParagraphStyle(
            "title", fontSize=14, alignment=TA_JUSTIFY, spaceAfter=0.2 * inch)
        ps_id = ParagraphStyle("id", fontSize=10)
        ps_pro = ParagraphStyle(
            'pro', fontSize=10, backColor='#27ae60', textColor="#FFFFFF", spaceBefore=7,borderPadding= (5,5,5,5))
        ps_con = ParagraphStyle(
            'con', fontSize=10, backColor='#c0392b', textColor='#FFFFFF',spaceBefore=7,borderPadding= (5,5,5,5))
        ps_need_info = ParagraphStyle(
            'need_info', fontSize=10, backColor='#000000', textColor='#FFFFFF',spaceBefore=7,borderPadding= (5,5,5,5))
        
        cover_page_title = ParagraphStyle("cover", fontSize=21, alignment=TA_CENTER, textColor="#000000")
        cover_page_subtitle = ParagraphStyle("cover", fontSize=16, spaceBefore= 15, alignment=TA_CENTER, textColor="#000000")

        contents.append(Spacer(0, 3 * inch))
        contents.append(Paragraph("Agenda Items - Comment Submissions",cover_page_title))
        contents.append(Paragraph(f"{datetime.fromtimestamp(agenda_items[0].agenda.meeting_time).strftime('%m/%d/%Y')} Council Meeting - Submissions for {today.strftime('%m/%d/%Y')}",cover_page_subtitle))
        contents.append(PageBreak())

        for upcoming_agenda_item in agenda_items:
            contents.append(
                Paragraph("Title: " + upcoming_agenda_item.title, ps_title))
            contents.append(
                Paragraph("ID: " + upcoming_agenda_item.agenda_item_id, ps_id)
            )
            pro_comments_on_agenda_item = Message.objects.filter(
                agenda_item=upcoming_agenda_item, pro=0
            )
            con_comments_on_agenda_item = Message.objects.filter(
                agenda_item=upcoming_agenda_item, pro=1
            )
            need_info_comments_on_agenda_item = Message.objects.filter(
                agenda_item=upcoming_agenda_item, pro=2
            )
            contents.append(Paragraph("Pro comments", ps_pro))
            contents.append(Spacer(1, 0.2 * inch))
            paragraphize_comments(pro_comments_on_agenda_item, contents)
            contents.append(Spacer(1, 0.5 * inch))
            contents.append(Paragraph("Con comments", ps_con))
            contents.append(Spacer(1, 0.2 * inch))
            paragraphize_comments(con_comments_on_agenda_item, contents)
            contents.append(Spacer(1, 0.5 * inch))
            contents.append(
                Paragraph("Need more information comments", ps_need_info))
            contents.append(Spacer(1, 0.2 * inch))
            paragraphize_comments(need_info_comments_on_agenda_item, contents)
            contents.append(Spacer(1, 0.5 * inch))
            contents.append(PageBreak())
        doc.build(contents)

        attachment_file_path = str(full_path) + "/Meeting_" + str(datetime.fromtimestamp(agenda_items[0].agenda.meeting_time).strftime('%Y%m%d')) + ".pdf"
        attachment_type = "application/pdf"
        attachment_name = "Agenda_Comments_Council_Meeting_" + str(datetime.fromtimestamp(agenda_items[0].agenda.meeting_time).strftime('%Y%m%d')) + f".pdf"

        email_body = """<html>
            <head>
                <style>
                    body {
                        font-family: sans-serif;
                        font-size: 12px;
                        color: #000;
                    }
                </style>
            </head>
            <body>
                <p>Greetings from Engage</p>
                <p>Please find attached the latest report for the upcoming Council Meeting.</p>
                <p>Thank you,</p>
                <p>Your Engage team</p>
                <hr>
                <p><i>This is an automated message, for any questions please contact <a hrek=mailto:contact@engage.town?subject=Feedback%20Agenda%20Comments%20Report>contact@engage.town</a></i></p>
            </body
        </html>
        """

        subject = f"Council Meeting {datetime.fromtimestamp(agenda_items[0].agenda.meeting_time).strftime('%m/%d/%Y')} - Agenda Recommendations, Comment Submissions for {today.strftime('%m/%d/%Y')}"
        recipient = Committee.objects.filter(name="Santa Monica City Council")[0]

        send_mail({"user":recipient,"subject":subject,"content":email_body,"attachment_file_path":attachment_file_path,"attachment_type":attachment_type,"attachment_file_name":attachment_name})
        
        return True
    except:
        return False