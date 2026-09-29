import smtplib
from email.mime.text import MIMEText

# --- CONFIGURAÇÕES ---
SMTP_SERVER = "://gmail.com"
SMTP_PORT = 587
EMAIL_USER = "gsoaressh@gmail.com"          # Mude para o seu e-mail
EMAIL_PASS = "wnwd qffs hwik wwlp"     # Mude para a sua senha de aplicativo
EMAIL_TO = "gsoaressh@gmail.com"       # Mude para o e-mail que vai receber

try:
    print("Tentando conectar ao servidor SMTP...")
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
    
    print("Enviando comando STARTTLS...")
    server.starttls()
    
    print("Tentando fazer login...")
    server.login(EMAIL_USER, EMAIL_PASS)
    
    # Criar mensagem simples
    msg = MIMEText("Este é um teste direto via script Python.")
    msg['Subject'] = "Teste de Conexão SMTP SMTP"
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    
    print("Enviando e-mail...")
    server.sendmail(EMAIL_USER, [EMAIL_TO], msg.as_string())
    server.quit()
    print("✅ Sucesso! O e-mail foi enviado.")

except Exception as e:
    print(f"\n❌ Erro ao conectar/enviar: {e}")
