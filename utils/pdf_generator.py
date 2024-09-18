from collections import defaultdict
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import Spacer
from utils.calculate_dues import calculate_dues


def generate_expense_report(expenses):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    elements.append(Paragraph("Expense Report<br/>", title_style))

    date_style = styles['Normal']
    date_style.alignment = TA_CENTER
    date_style.fontName = 'Helvetica'
    date_style.fontSize = 12
    start_date = min(expenses[username][0].date for username in expenses)
    end_date = max(expenses[username][0].date for username in expenses)
    elements.append(Paragraph(
        f"<i>({start_date.strftime('%d %b, %Y')} - {end_date.strftime('%d %b, %Y')})</i>", date_style))

    elements.append(Spacer(1, 0.1*inch))

    total_spent = 0
    for username, user_expenses in expenses.items():
        elements.append(
            Paragraph(f"Expenses by @{username}", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))

        expenses_by_date = defaultdict(list)
        for exp in user_expenses:
            expenses_by_date[exp.date.strftime('%d %b, %Y')].append(exp)

        data = [["Date", "Item", "Price"]]
        total_amount = 0
        for date, exps in sorted(expenses_by_date.items()):
            for exp in exps:
                # Wrap the item text in a Paragraph to allow for text wrapping
                item_paragraph = Paragraph(exp.item, styles['BodyText'])
                data.append([date, item_paragraph, f"৳{exp.price:.2f}"])
                total_amount += exp.price

        total_spent += total_amount

        # Add total amount row
        data.append(
            ["", Paragraph("<b>Total</b>", styles['BodyText']), f"৳{total_amount:.2f}"])

        # Define column widths (make the date column compact)
        col_widths = [1.1*inch, 4*inch, 1.7*inch]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.hAlign = 'LEFT'

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all cells to the left
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font bold
            ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for the header
            # Background color for the rest
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.whitesmoke, colors.lightgrey]),  # Alternate row colors
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Text color
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Body text font
            ('FONTSIZE', (0, 1), (-1, -1), 10),  # Body font size
            ('TOPPADDING', (0, 1), (-1, -1), 6),  # Padding for body rows
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            # Grid line for all cells
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # Background for total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Bold total row
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))

    # Add summary table
    elements.append(Paragraph("Summary", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    dues_summary = calculate_dues(expenses)
    num_users = len(dues_summary)
    per_head_amount = total_spent / num_users

    summary_data = [
        ["Total Spent", f"৳{total_spent:.2f}"],
        ["Number of Users", str(num_users)],
        ["Per Head Amount", f"৳{per_head_amount:.2f}"]
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.hAlign = 'LEFT'
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.2*inch))

    # Add owes/gets table
    elements.append(Paragraph("Owes/Gets", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))
    # Add note about calculation
    note = "Delta = abs(Per Head Amount - Spent by Member)<br/>" \
           "• Gets Delta if Per Head Amount > Spent by Member<br/>" \
           "• Owes Delta if Per Head Amount < Spent by Member<br/>"
    note_style = styles['Normal'].clone('NoteStyle')
    note_style.bulletIndent = 12
    note_style.fontSize = 10
    note_style.fontName = 'Helvetica'
    note_style.alignment = TA_LEFT
    elements.append(Paragraph(note, note_style))
    elements.append(Spacer(1, 0.2*inch))

    owes_gets_data = [["Member", "Amount"]]
    for due in dues_summary:
        due = due.lstrip('😎 ')
        member, status, amount = due.split(" ")
        owes_gets_data.append([f"{member} {status}", amount])

    owes_gets_table = Table(owes_gets_data, colWidths=[3*inch, 3*inch])
    owes_gets_table.hAlign = 'LEFT'
    owes_gets_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.lightgrey]),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(owes_gets_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
