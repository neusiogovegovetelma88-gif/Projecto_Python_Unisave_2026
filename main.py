"""
PROJECTO: Ciber Seguro - Quiz de Segurança Informática
UNISAVE - Universidade Save | Faculdade de Engenharia e Tecnologia
Curso: Ciências da Computação | Disciplina:PTP I - Programação I
Ano: 2026
Desenvolvedores: Clara Pinto Covane, Dionisío João Rungo, Neusio da Telma Gove, Frédio Vasco Utui
"""
import json
import os
import random
import tkinter as tk
from tkinter import messagebox
from datetime import date
from dataclasses import dataclass, field

FICHEIRO_HISTORICO = os.path.join(os.path.expanduser("~"), ".ciber_seguro.json")

@dataclass
class Pergunta:
    texto: str
    opcoes: list
    resposta_certa: int
    explicacao: str
    recomendacao: str

@dataclass
class Tema:
    id: str
    nome: str
    icone: str
    cor: str
    perguntas: list = field(default_factory=list)

def carregar_temas():
    dados = [
        ("basico", "Cibersegurança básica", "🔐", "#3498DB", [
            ("O que é phishing?", ["Um vírus que apaga ficheiros", "Uma tentativa de enganar a pessoa para revelar dados", "Uma ligação Wi-Fi lenta", "Um tipo de antivírus"], 1, "Phishing usa mensagens falsas para roubar senhas e dados.", "Não clique em links de mensagens inesperadas."),
            ("Recebeu uma mensagem do 'banco' a pedir o seu PIN. O que faz?", ["Responde com o PIN", "Ignora e contacta o banco pelo número oficial", "Reencaminha aos amigos", "Clica no link para ver"], 1, "Nenhum banco legítimo pede PIN por mensagem.", "Nunca partilhe PIN ou códigos de verificação."),
            ("Qual destes é um sinal de mensagem fraudulenta?", ["Trata-o pelo nome correcto", "Cria urgência: 'a sua conta será bloqueada hoje'", "Vem de um contacto conhecido", "Não tem links"], 1, "A pressão serve para o impedir de pensar antes de agir.", "Quando houver urgência, pare e confirme por outro canal."),
            ("Com que frequência deve actualizar o telemóvel?", ["Nunca", "Só quando avaria", "Sempre que houver actualização", "Uma vez por ano"], 2, "As actualizações corrigem falhas que os atacantes já conhecem.", "Active as actualizações automáticas."),
            ("Quantos e-mails de phishing são enviados por dia no mundo?", ["Alguns", "Um par", "Milhares de milhões", "3 ou 4"], 2, "São milhares de milhões por dia, todos somos alvos.", "Crie o hábito de desconfiar."),
            ("O que é engenharia social?", ["Um tipo de computador", "Manipular pessoas para obter informações secretas", "Um programa antivírus", "Uma rede Wi-Fi"], 1, "O atacante usa conversa e confiança, não só vírus.", "Desconfie de quem pede dados urgentes."),
            ("Recebeu um anexo estranho de um desconhecido. O que faz?", ["Abre logo", "Não abre e apaga a mensagem", "Reencaminha", "Abre noutro telemóvel"], 1, "Anexos podem ter vírus escondidos.", "Não abra anexos de quem não conhece."),
            ("Para que serve uma cópia de segurança (backup)?", ["Para gastar espaço", "Para recuperar ficheiros se perder ou for atacado", "Para deixar o telemóvel lento", "Para nada"], 1, "Se perder o telemóvel ou for atacado, recupera os dados.", "Faça backup das fotos e documentos importantes."),
            ("Alguém pede foto do seu BI para 'confirmar um prémio'. O que faz?", ["Envia a foto", "Não envia, é uma tentativa de roubo de identidade", "Envia só a frente", "Envia e depois apaga"], 1, "Com o BI podem abrir contas em seu nome.", "Nunca envie foto de documentos a estranhos."),
            ("O que é um antivírus?", ["Um jogo", "Um programa que detecta e remove programas maliciosos", "Uma rede social", "Um tipo de senha"], 1, "Ele protege contra vírus e programas perigosos.", "Mantenha o antivírus actualizado."),
            ("O que deve fazer se receber um e-mail com erro de português e link estranho?", ["Clicar para ver", "Desconfiar e não clicar", "Responder a perguntar", "Reencaminhar"], 1, "Erros e links estranhos são sinais de phishing.", "Verifique o remetente antes de clicar."),
            ("O que é uma senha segura?", ["Data de nascimento", "Nome do filho", "Frase longa com letras, números e símbolos", "123456"], 2, "Frases longas são difíceis de adivinhar.", "Use frases longas como senha."),
            ("Deve partilhar a sua localização em tempo real nas redes sociais?", ["Sim, sempre", "Não, pode atrair criminosos", "Só com estranhos", "Sim, se for de noite"], 1, "Partilhar localização mostra onde está.", "Evite partilhar localização em tempo real."),
            ("O que fazer se um desconhecido pede para instalar um programa no seu PC?", ["Instalar logo", "Recusar e desligar", "Instalar e depois apagar", "Dar o controlo"], 1, "Pode ser controlo remoto para roubar dados.", "Nunca deixe estranhos controlar o seu PC."),
            ("Porque não deve usar computadores públicos para o banco?", ["Porque são lentos", "Outros podem ver a sua senha", "Porque não têm internet", "Porque são velhos"], 1, "Computadores públicos podem ter programas espiões.", "Use só o seu aparelho para o banco."),
        ]),
        ("virus", "Vírus e fraudes", "🦠", "#E74C3C", [
            ("Qual é a forma mais comum de apanhar um vírus?", ["Carregar o telemóvel", "Instalar apps de fontes desconhecidas", "Usar o modo avião", "Limpar a cache"], 1, "APKs fora da loja e anexos suspeitos são as portas de entrada.", "Instale só da loja oficial."),
            ("O que faz um ransomware?", ["Acelera o computador", "Bloqueia os ficheiros e exige pagamento", "Apaga a cache", "Mostra anúncios"], 1, "Cifra os seus dados e pede dinheiro para os devolver.", "Faça cópias de segurança regulares."),
            ("'Ganhou um prémio! Envie 500 MT para o levantar.' É...", ["Um prémio verdadeiro", "Uma fraude", "Uma promoção", "Um erro do sistema"], 1, "Prémios verdadeiros não exigem pagamento antecipado.", "Nunca pague para receber um prémio."),
            ("Alguém liga a pedir um código recebido por SMS. Deve...", ["Dar o código", "Desligar e não partilhar o código", "Dar só metade", "Pedir o número e dar"], 1, "Esse código dá acesso à sua conta. Ninguém legítimo o pede.", "Códigos são pessoais."),
            ("Como confirma se um site de compras é fiável?", ["Tem muitas cores", "Usa HTTPS, tem contactos reais e boas avaliações", "Tem preços muito baixos", "Foi partilhado num grupo"], 1, "Preços demasiado baixos são isco habitual.", "Pesquise o nome da loja + 'burla' antes de comprar."),
            ("O que é um cavalo de Troia (Trojan)?", ["Um animal", "Um programa que parece útil mas esconde vírus", "Um antivírus", "Uma senha forte"], 1, "Parece um jogo ou app normal, mas rouba dados.", "Desconfie de apps milagrosas e grátis."),
            ("O seu telemóvel começou a mostrar muitos anúncios sozinho. Pode ser...", ["Normal", "Um vírus / app maliciosa instalada", "Bateria fraca", "Internet lenta"], 1, "Anúncios em excesso são sinal de app maliciosa.", "Desinstale apps que não reconhece."),
            ("Clicou num link 'Ganhou um iPhone!' O que deve fazer de imediato?", ["Preencher os dados", "Fechar a página e não dar dados", "Partilhar com amigos", "Pagar o envio"], 1, "É isco para roubar dados e dinheiro.", "Feche páginas de prémios falsos."),
            ("O que é um link encurtado suspeito?", ["Um link curto que esconde o destino real", "Um link rápido e seguro", "Um link do banco", "Um link sem vírus"], 0, "Links curtos escondem para onde vão realmente.", "Não clique em links curtos de estranhos."),
            ("Um amigo manda 'vê esta foto' com um ficheiro estranho. O que faz?", ["Abre logo", "Pergunta ao amigo se foi ele que mandou antes de abrir", "Abre e reencaminha", "Ignora o amigo"], 1, "Contas hackeadas mandam vírus aos contactos.", "Confirme com o amigo por outro canal."),
            ("O que é um vírus de computador?", ["Um programa que se espalha e danifica", "Um tipo de internet", "Um antivírus", "Uma senha"], 0, "Vírus espalham-se e danificam ficheiros.", "Mantenha antivírus activo."),
            ("Recebeu SMS a dizer que a sua conta será bloqueada. O que faz?", ["Clica no link", "Ignora e vai à app oficial", "Envia dados", "Liga ao número do SMS"], 1, "SMS falsos usam medo para roubar.", "Vá sempre à app oficial, não ao link."),
            ("O que é smishing?", ["Phishing por SMS", "Um jogo", "Um tipo de Wi-Fi", "Uma senha"], 0, "Smishing é phishing por mensagem de texto.", "Desconfie de SMS com links."),
            ("Deve pagar o resgate se for atacado por ransomware?", ["Sim", "Não, pode não recuperar e incentiva o crime", "Sim, logo", "Sim, metade"], 1, "Pagar não garante recuperação.", "Faça backup e denuncie."),
            ("Um site pede para desactivar o antivírus para descarregar. O que faz?", ["Desactiva", "Não descarrega, é perigoso", "Desactiva e depois activa", "Pede ao amigo"], 1, "Sites sérios nunca pedem isso.", "Nunca desactive o antivírus para descarregar."),
        ]),
        ("wifi", "Segurança das redes Wi-Fi", "📶", "#1ABC9C", [
            ("Qual é o maior risco numa rede Wi-Fi pública aberta?", ["Gastar bateria", "Alguém intercetar o que envia", "O sinal ser fraco", "Nenhum"], 1, "Outras pessoas podem observar o tráfego ou criar redes falsas.", "Evite o banco em Wi-Fi público. Use dados móveis."),
            ("Qual segurança Wi-Fi é mais recomendada em casa?", ["Sem senha", "WEP", "WPA2 ou WPA3", "Qualquer um"], 2, "WPA2 e WPA3 são os padrões actuais. WEP é fácil de quebrar.", "No router, use WPA2/WPA3 com senha longa."),
            ("O que deve fazer à senha original do router?", ["Mantê-la", "Alterá-la logo na instalação", "Colá-la no router", "Partilhá-la"], 1, "Senhas de fábrica seguem padrões conhecidos.", "Mude a senha do Wi-Fi e do router."),
            ("Existem duas redes com nomes quase iguais num café. Como agir?", ["Ligar à mais forte", "Perguntar qual é a rede oficial", "Ligar às duas", "Ligar à sem senha"], 1, "Redes falsas com nomes parecidos roubam dados.", "Confirme o nome exacto com o responsável."),
            ("Desligar Wi-Fi e Bluetooth quando não usa ajuda a...", ["Nada", "Reduzir exposição a ligações indesejadas", "Aumentar velocidade", "Apagar vírus"], 1, "Ligações automáticas podem ligar a redes inseguras.", "Desactive a ligação automática a redes abertas."),
            ("O que é uma VPN?", ["Um vírus", "Uma ferramenta que protege a sua ligação", "Uma rede social", "Um tipo de senha"], 1, "A VPN cifra a sua ligação em redes públicas.", "Use VPN se precisar de usar Wi-Fi público."),
            ("O que significa o cadeado ao lado do endereço do site?", ["O site é bonito", "A ligação é protegida (HTTPS)", "O site é grátis", "O site é do governo"], 1, "O cadeado mostra que a ligação está cifrada.", "Só coloque senhas em sites com cadeado."),
            ("Deve fazer operações bancárias num Wi-Fi público?", ["Sim, é seguro", "Não, use dados móveis", "Sim, se for rápido", "Sim, se ninguém estiver a ver"], 1, "Redes públicas podem ser espiadas.", "Faça banco só com dados móveis ou rede de confiança."),
            ("Porque não deve deixar o Wi-Fi sempre ligado a ligar sozinho?", ["Gasta bateria", "Pode ligar a uma rede falsa sem reparar", "Fica mais lento", "Não há problema"], 1, "O telemóvel pode ligar a uma rede falsa com nome igual.", "Desactive a ligação automática."),
            ("Alguém pede a senha do seu Wi-Fi em casa. O que faz?", ["Dá logo", "Só dá a quem confia e depois pode mudar", "Escreve no Facebook", "Deixa sem senha"], 1, "Quem tem a senha pode ver os seus aparelhos.", "Partilhe a senha só com quem confia."),
            ("O que é uma rede Wi-Fi falsa (Evil Twin)?", ["Uma rede gémea que imita a verdadeira", "Uma rede mais rápida", "Uma rede do governo", "Uma rede sem nome"], 0, "Imita a rede verdadeira para roubar dados.", "Confirme sempre o nome da rede."),
            ("Deve deixar o Bluetooth sempre ligado em locais públicos?", ["Sim", "Não, desligue quando não usar", "Sim, se for novo", "Sim, à noite"], 1, "Bluetooth ligado pode ser explorado.", "Desligue o Bluetooth quando não usar."),
            ("O que fazer se o seu Wi-Fi de casa ficar muito lento de repente?", ["Ignorar", "Verificar quem está ligado e mudar a senha", "Desligar para sempre", "Dar a senha a todos"], 1, "Pode haver intrusos a usar.", "Mude a senha e veja aparelhos ligados."),
            ("É seguro usar Wi-Fi sem senha num aeroporto?", ["Sim", "Não, qualquer pessoa pode espiar", "Sim, se for rápido", "Sim, se tiver cadeado"], 1, "Redes abertas não cifram os dados.", "Use dados móveis no aeroporto."),
            ("Porque deve esconder o nome da sua rede Wi-Fi?", ["Para ficar bonito", "Para dificultar que estranhos a encontrem", "Para gastar menos", "Não deve"], 1, "Rede escondida é menos visível.", "Considere esconder o SSID e usar senha forte."),
        ]),
        ("contas", "Protecção de contas", "🔑", "#F39C12", [
            ("Qual destas é a senha mais forte?", ["123456", "dionisio2005", "Tr0nc0-Azul-Chuva-47!", "senha"], 2, "Senhas longas com várias palavras e símbolos são mais difíceis.", "Use senhas com 12+ caracteres."),
            ("Pode usar a mesma senha em várias contas?", ["Sim, é mais fácil", "Não, se uma for roubada as outras ficam expostas", "Só em redes sociais", "Só no e-mail"], 1, "Atacantes testam a mesma senha noutros sites.", "Use uma senha diferente por conta."),
            ("O que é a autenticação em dois passos (2FA)?", ["Digitar a senha duas vezes", "Um segundo passo além da senha", "Ter duas contas", "Mudar a senha todos os dias"], 1, "Mesmo com a senha roubada, falta o segundo factor.", "Active o 2FA no e-mail, WhatsApp e banco."),
            ("Onde deve guardar as suas senhas?", ["Num papel no ecrã", "Numa nota sem protecção", "Num gestor de senhas", "Num grupo de WhatsApp"], 2, "Gestores cifram os dados e geram senhas únicas.", "Evite guardar senhas em locais visíveis."),
            ("Suspeita que a conta foi invadida. Primeiro passo?", ["Esperar", "Mudar a senha e terminar sessões abertas", "Apagar a conta", "Avisar amanhã"], 1, "Mudar a senha corta o acesso do atacante.", "Verifique também o e-mail e número de recuperação."),
            ("Recebeu alerta de login estranho na sua conta. O que faz?", ["Ignora", "Muda a senha logo e verifica os aparelhos ligados", "Apaga o alerta", "Manda o alerta aos amigos"], 1, "Pode ser alguém a tentar entrar.", "Verifique aparelhos ligados e mude a senha."),
            ("Deixou a sessão aberta num computador público. O que pode acontecer?", ["Nada", "Outra pessoa pode entrar na sua conta", "O computador apaga", "A conta fica mais segura"], 1, "Quem vier a seguir fica com a sua conta aberta.", "Termine sempre a sessão em computadores públicos."),
            ("Qual é o risco de usar a data de nascimento como senha?", ["Nenhum", "É fácil de adivinhar", "É muito forte", "É proibido"], 1, "Datas de nascimento estão no BI e redes sociais.", "Não use datas pessoais como senha."),
            ("Como protege melhor o seu WhatsApp?", ["Sem senha", "Com verificação em duas etapas e PIN", "Só com foto", "Deixar aberto"], 1, "A verificação em duas etapas impede roubo da conta.", "Active a verificação em duas etapas no WhatsApp."),
            ("Esqueceu a senha e pedem para enviar o código de recuperação a outra pessoa. Deve...", ["Enviar", "Não enviar, o código é só seu", "Enviar metade", "Enviar e depois mudar"], 1, "Quem tem o código toma a sua conta.", "Nunca partilhe códigos de recuperação."),
            ("Deve partilhar a sua senha com o melhor amigo?", ["Sim", "Não, senha é pessoal", "Sim, se ele pedir", "Sim, se for urgente"], 1, "Senha partilhada deixa de ser segura.", "Nunca partilhe a sua senha."),
            ("O que é um gestor de senhas?", ["Um caderno", "Uma app que guarda senhas de forma segura", "Um grupo de WhatsApp", "Um papel"], 1, "Guarda e gera senhas fortes.", "Use um gestor de senhas."),
            ("Recebeu e-mail a dizer 'mude a senha aqui'. O que faz?", ["Clica logo", "Vai à app oficial e muda lá", "Responde com a senha", "Ignora para sempre"], 1, "Links podem ser falsos.", "Mude a senha só na app oficial."),
            ("Porque deve mudar a senha se houve fuga de dados?", ["Para gastar tempo", "Porque a sua senha pode estar na internet", "Porque é moda", "Não deve"], 1, "Senhas vazadas são vendidas.", "Mude a senha após fugas de dados."),
            ("O que fazer se já não usa uma conta antiga?", ["Deixar lá", "Apagar ou fechar a conta", "Dar a senha", "Esquecer"], 1, "Contas abandonadas podem ser hackeadas.", "Feche contas que já não usa."),
        ]),
    ]
    temas = []
    for id_t, nome, ico, cor, qs in dados:
        perguntas = [Pergunta(*q) for q in qs]
        temas.append(Tema(id_t, nome, ico, cor, perguntas))
    return temas

TEMAS = carregar_temas()

class GestorHistorico:
    @staticmethod
    def carregar():
        try:
            with open(FICHEIRO_HISTORICO, encoding="utf-8") as f:
                dados = json.load(f)
                if not isinstance(dados, dict):
                    return {}
                return dados
        except (OSError, ValueError):
            return {}
    @staticmethod
    def guardar(dados):
        try:
            with open(FICHEIRO_HISTORICO, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
                return True
        except OSError:
            return False
    @staticmethod
    def registar(tema_id, pontos, total):
        dados = GestorHistorico.carregar()
        entrada = dados.get(tema_id, {"tentativas": 0, "melhor": 0, "log": []})
        entrada["tentativas"] += 1
        entrada["melhor"] = max(entrada["melhor"], pontos)
        novo = {"s": pontos, "t": total, "d": date.today().strftime("%d/%m/%Y")}
        entrada["log"] = [novo] + entrada["log"][:9]
        dados[tema_id] = entrada
        GestorHistorico.guardar(dados)

BG = "#FFFFFF"
BG_CARD = "#F2F2F2"
TEXTO = "#1A1A1A"
TEXTO_CINZA = "#666666"
AMARELO = "#E67E22"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ciber Seguro - UNISAVE")
        self.root.geometry("900x650")
        self.root.minsize(700, 550)
        self.root.resizable(True, True)
        self.root.configure(bg=BG)
        self.tema = None
        self.perguntas = []
        self.idx = 0
        self.pontos = 0
        self.erradas = []
        self.mostrar_menu()

    def limpar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def mostrar_menu(self):
        self.limpar()
        tk.Label(self.root, text="🛡️ CIBER SEGURO", font=("Helvetica", 26, "bold"), fg=TEXTO, bg=BG).pack(pady=(20, 0))
        tk.Label(self.root, text="UNISAVE • Aprenda a proteger-se de burlas e vírus", font=("Helvetica", 11), fg=TEXTO_CINZA, bg=BG).pack()
        tk.Label(self.root, text="Escolha um tema para começar:", font=("Helvetica", 13, "bold"), fg=AMARELO, bg=BG).pack(pady=15)
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True, padx=25, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        for i, t in enumerate(TEMAS):
            linha = i // 2
            coluna = i % 2
            tk.Button(frame, text=f"{t.icone}\n{t.nome}", font=("Helvetica", 14, "bold"), bg=t.cor, fg="white", wraplength=300, command=lambda tema=t: self.comecar(tema)).grid(row=linha, column=coluna, sticky="nsew", padx=10, pady=10)
        frame2 = tk.Frame(self.root, bg=BG)
        frame2.pack(fill="x", padx=25, pady=(0, 20))
        tk.Button(frame2, text="📊 Ver Histórico", font=("Helvetica", 11), bg="#34495E", fg="white", height=2, command=self.mostrar_historico).pack(side="left", fill="x", expand=True, padx=(0, 5))
        tk.Button(frame2, text="👥 Sobre o Projeto", font=("Helvetica", 11), bg="#3498DB", fg="white", height=2, command=self.mostrar_sobre).pack(side="left", fill="x", expand=True, padx=(5, 5))
        tk.Button(frame2, text="❌ Sair", font=("Helvetica", 11), bg="#E74C3C", fg="white", height=2, command=self.root.quit).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def mostrar_sobre(self):
        self.limpar()
        # Canvas + Scrollbar para caber tudo
        canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scroll_frame, text="🛡️ CIBER SEGURO", font=("Helvetica", 20, "bold"), fg=TEXTO, bg=BG).pack(pady=(15, 0))
        tk.Label(scroll_frame, text="UNISAVE • Faculdade de Engenharia e Tecnologia\nCiências da Computação • Python / Programação • 2026", font=("Helvetica", 10), fg=TEXTO_CINZA, bg=BG, justify="center").pack(pady=5)

        def titulo(t):
            tk.Label(scroll_frame, text=t, font=("Helvetica", 13, "bold"), fg=AMARELO, bg=BG, anchor="w").pack(fill="x", padx=25, pady=(15, 2))
        def texto(t):
            tk.Label(scroll_frame, text=t, font=("Helvetica", 11), fg=TEXTO, bg=BG, wraplength=650, justify="left", anchor="w").pack(fill="x", padx=25, pady=2)

        titulo("📝 Descrição do Projeto")
        texto("O Ciber Seguro é uma aplicação desktop em Python que ensina Cibersegurança de forma simples e divertida, através de um quiz interactivo. Foi desenvolvido para ajudar estudantes, jovens e utilizadores comuns a reconhecerem burlas, vírus, phishing e outros perigos da internet, e a aprenderem como se proteger no dia a dia.")

        titulo("❓ Problema que Resolve")
        texto("Muitas pessoas em Moçambique perdem dinheiro e contas todos os dias por causa de mensagens falsas a pedir PIN e códigos do banco, prémios falsos tipo 'Ganhou um iPhone, envie 500 MT', links de phishing no WhatsApp e SMS, Wi-Fi público sem protecção e senhas fracas e iguais em todas as contas. A maioria não sabe identificar esses ataques.")
        texto("O nosso projeto resolve isso ensinando na prática: a pessoa joga, erra, recebe a explicação correcta e uma recomendação para não voltar a cair.")

        titulo("✨ Funcionalidades")
        texto("• 4 temas com 15 perguntas cada, total 60 perguntas: Cibersegurança básica, Vírus e fraudes, Segurança das redes Wi-Fi, Protecção de contas\n• Perguntas e respostas baralhadas\n• Feedback imediato com explicação da resposta certa\n• Resultado em percentagem + recomendações personalizadas\n• Histórico guardado em JSON: melhor nota, tentativas e datas\n• Interface gráfica com Tkinter, fundo branco")

        titulo("👥 Elementos do Grupo")
        texto("• Clara Pinto Covane (@claracovane1)\n• Dionisío João Rungo (@dionisiorungo8-max)\n• Neusio da Telma Gove (@neusiogovegovetelma88)\n• Frédio Vasco Utui (@frediovascoutui8)")

        titulo("🛠️ Tecnologias")
        texto("Python 3 • Tkinter • JSON • Random • Git e GitHub")

        tk.Button(scroll_frame, text="⬅ Voltar ao Menu", font=("Helvetica", 11), bg="#34495E", fg="white", width=30, command=self.mostrar_menu).pack(pady=20)

    def comecar(self, tema):
        self.tema = tema
        self.perguntas = tema.perguntas[:]
        random.shuffle(self.perguntas)
        self.idx = 0
        self.pontos = 0
        self.erradas = []
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        self.limpar()
        q = self.perguntas[self.idx]
        tk.Label(self.root, text=f"{self.tema.icone} {self.tema.nome}  •  Pergunta {self.idx+1}/{len(self.perguntas)}", font=("Helvetica", 10, "bold"), fg=AMARELO, bg=BG).pack(pady=15)
        tk.Label(self.root, text=f"Pontos: {self.pontos}", font=("Helvetica", 11), fg=TEXTO, bg=BG).pack()
        tk.Label(self.root, text=q.texto, font=("Helvetica", 14, "bold"), fg=TEXTO, bg=BG, wraplength=620, justify="center").pack(pady=25, padx=20)
        ordem = list(range(len(q.opcoes)))
        random.shuffle(ordem)
        self.ordem_atual = ordem
        self.pergunta_atual = q
        letras = "ABCD"
        for k, orig in enumerate(ordem):
            tk.Button(self.root, text=f"{letras[k]})  {q.opcoes[orig]}", font=("Helvetica", 11), bg=BG_CARD, fg=TEXTO, width=55, height=2, wraplength=500, anchor="w", command=lambda o=orig: self.responder(o)).pack(pady=4)
        tk.Button(self.root, text="⬅ Voltar ao Menu", font=("Helvetica", 10), bg="#34495E", fg="white", command=self.mostrar_menu).pack(pady=20)

    def responder(self, escolha):
        q = self.pergunta_atual
        if escolha == q.resposta_certa:
            self.pontos += 1
            messagebox.showinfo("✅ Correcto!", q.explicacao)
        else:
            self.erradas.append(q)
            letras = "ABCD"
            certa_letra = letras[self.ordem_atual.index(q.resposta_certa)]
            messagebox.showerror("❌ Incorrecto", f"A resposta certa era {certa_letra}.\n\n{q.explicacao}")
        self.idx += 1
        if self.idx < len(self.perguntas):
            self.mostrar_pergunta()
        else:
            self.mostrar_resultado()

    def mostrar_resultado(self):
        self.limpar()
        total = len(self.perguntas)
        perc = round(self.pontos/total*100) if total else 0
        tk.Label(self.root, text="🏁 RESULTADO", font=("Helvetica", 20, "bold"), fg=TEXTO, bg=BG).pack(pady=20)
        tk.Label(self.root, text=f"{self.pontos}/{total}  •  {perc}%", font=("Helvetica", 28, "bold"), fg=AMARELO, bg=BG).pack()
        msg = "🎉 Perfeito! És um expert!" if perc == 100 else "👍 Bom! Revê as recomendações." if perc >= 60 else "⚠️ Precisas de ter mais cuidado online."
        tk.Label(self.root, text=msg, font=("Helvetica", 12), fg=TEXTO, bg=BG).pack(pady=10)
        if self.erradas:
            tk.Label(self.root, text="📌 Recomendações para ti:", font=("Helvetica", 12, "bold"), fg=AMARELO, bg=BG).pack(pady=(15,5))
            for q in self.erradas:
                tk.Label(self.root, text=f"• {q.recomendacao}", font=("Helvetica", 10), fg=TEXTO, bg=BG, wraplength=600, justify="left").pack(pady=2, padx=20, anchor="w")
        GestorHistorico.registar(self.tema.id, self.pontos, total)
        tk.Button(self.root, text="🔄 Jogar Novamente", font=("Helvetica", 12, "bold"), bg="#1ABC9C", fg="white", width=30, command=lambda: self.comecar(self.tema)).pack(pady=(20,5))
        tk.Button(self.root, text="🏠 Menu Principal", font=("Helvetica", 11), bg="#34495E", fg="white", width=30, command=self.mostrar_menu).pack(pady=5)

    def mostrar_historico(self):
        self.limpar()
        d = GestorHistorico.carregar()
        tk.Label(self.root, text="📊 HISTÓRICO", font=("Helvetica", 20, "bold"), fg=TEXTO, bg=BG).pack(pady=20)
        if not d:
            tk.Label(self.root, text="Ainda não fizeste nenhum quiz.", font=("Helvetica", 12), fg=TEXTO_CINZA, bg=BG).pack(pady=20)
        else:
            for t in TEMAS:
                e = d.get(t.id)
                if e:
                    ult = ", ".join(f"{l['s']}/{l['t']} ({l['d']})" for l in e["log"][:3])
                    tk.Label(self.root, text=f"{t.icone} {t.nome}", font=("Helvetica", 12, "bold"), fg=AMARELO, bg=BG).pack(pady=(10,0), padx=30, anchor="w")
                    tk.Label(self.root, text=f"Melhor: {e['melhor']}/{len(t.perguntas)}  •  Tentativas: {e['tentativas']}\nÚltimos: {ult}", font=("Helvetica", 11), fg=TEXTO, bg=BG, justify="left").pack(padx=30, anchor="w")
        tk.Button(self.root, text="🗑️ Apagar Histórico", font=("Helvetica", 11), bg="#E74C3C", fg="white", width=30, command=lambda: [GestorHistorico.guardar({}), self.mostrar_historico()]).pack(pady=(20,5))
        tk.Button(self.root, text="⬅ Voltar", font=("Helvetica", 11), bg="#34495E", fg="white", width=30, command=self.mostrar_menu).pack(pady=5)

def main():
    try:
        root = tk.Tk()
        App(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()