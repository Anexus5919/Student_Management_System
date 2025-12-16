from reportlab.pdfgen import canvas

c = canvas.Canvas("Student_Management_System_Report.pdf")
t = c.beginText(40,800)
t.setFont("Helvetica",11)

for l in [
    "Student Management System",
    "",
    "Modules:",
    "Login / Authentication",
    "Dashboard with Summary Panels",
    "CRUD + Search + Sort",
    "Analytics Dashboard",
    "CSV & PDF Export",
    "",
    "Conclusion:",
    "A professional Python GUI application with database connectivity."
]:
    t.textLine(l)

c.drawText(t)
c.save()
