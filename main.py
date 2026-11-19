"""

PROJECTO: Ciber Seguro - Quiz de Segurança Informática
UNISAVE - Universidade Save | Faculdade de Engenharia e Tecnologia
Curso: Ciências da Computação | Disciplina: Python / Programação
Ano: 2026

DESCRIÇÃO:
Aplicação desktop em Python que ensina cibersegurança de forma
interativa. O utilizador escolhe um tema, responde a um quiz de
5 perguntas, recebe explicação imediata e recomendações de
segurança. O progresso é guardado localmente em JSON.

PROBLEMA QUE RESOLVE:
Muitas pessoas em Moçambique caem em phishing, burlas de prémios,
roubo de PIN e Wi-Fi falso por falta de conhecimento básico.
O Ciber Seguro ensina a identificar e evitar esses golpes.

FUNCIONALIDADES:
- 4 temas, 20 perguntas
- Perguntas e respostas baralhadas
- Feedback imediato com explicação
- Resultado em % + recomendações personalizadas
- Histórico guardado em JSON (melhor nota, tentativas, datas)

Grupo - 4 elementos (ver README.md)
Autores: Clara Pinto Covane
         Dionisío João Rungo
         Neusio da Telma Gove
         Frédio Vasco Utui
"""
import json
import os
import random
import tkinter as tk
from tkinter import messagebox
from datetime import date
from dataclasses import dataclass, field

FICHEIRO_HISTORICO = os.path.join(os.path.expanduser("~"), ".ciber_seguro.json")

# ---------------- MODELO DE DADOS (POO) ----------------

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
    """Cria os temas a partir dos dados. Manipulação de dados em lista."""
    dados = [
        ("basico", "Cibersegurança básica", "🔐", "#3498DB", [
            ("O que é phishing?", ["Um vírus que apaga ficheiros", "Uma tentativa de enganar a pessoa para revelar dados", "Uma ligação Wi-Fi lenta", "Um tipo de antivírus"], 1, "Phishing usa mensagens falsas para roubar senhas e dados.", "Não clique em links de mensagens inesperadas."),
            ("Recebeu uma mensagem do 'banco' a pedir o seu PIN. O que faz?", ["Responde com o PIN", "Ignora e contacta o banco pelo número oficial", "Reencaminha aos amigos", "Clica no link para ver"], 1, "Nenhum banco legítimo pede PIN por mensagem.", "Nunca partilhe PIN ou códigos de verificação."),
            ("Qual destes é um sinal de mensagem fraudulenta?", ["Trata-o pelo nome correcto", "Cria urgência: 'a sua conta será bloqueada hoje'", "Vem de um contacto conhecido", "Não tem links"], 1, "A pressão serve para o impedir de pensar antes de agir.", "Quando houver urgência, pare e confirme por outro canal."),
            ("Com que frequência deve actualizar o telemóvel?", ["Nunca", "Só quando avaria", "Sempre que houver actualização", "Uma vez por ano"], 2, "As actualizações corrigem falhas que os atacantes já conhecem.", "Active as actualizações automáticas."),
            ("Quantos e-mails de phishing são enviados por dia no mundo?", ["Alguns", "Um par", "Milhares de milhões", "3 ou 4"], 2, "São milhares de milhões por dia, todos somos alvos.", "Crie o hábito de desconfiar."),
        ]),
        ("virus", "Vírus e fraudes", "🦠", "#E74C3C", [
            ("Qual é a forma mais comum de apanhar um vírus?", ["Carregar o telemóvel", "Instalar apps de fontes desconhecidas", "Usar o modo avião", "Limpar a cache"], 1, "APKs fora da loja e anexos suspeitos são as portas de entrada.", "Instale só da loja oficial."),
            ("O que faz um ransomware?", ["Acelera o computador", "Bloqueia os ficheiros e exige pagamento", "Apaga a cache", "Mostra anúncios"], 1, "Cifra os seus dados e pede dinheiro para os devolver.", "Faça cópias de segurança regulares."),
            ("'Ganhou um prémio! Envie 500 MT para o levantar.' É...", ["Um prémio verdadeiro", "Uma fraude", "Uma promoção", "Um erro do sistema"], 1, "Prémios verdadeiros não exigem pagamento antecipado.", "Nunca pague para receber um prémio."),
            ("Alguém liga a pedir um código recebido por SMS. Deve...", ["Dar o código", "Desligar e não partilhar o código", "Dar só metade", "Pedir o número e dar"], 1, "Esse código dá acesso à sua conta. Ninguém legítimo o pede.", "Códigos são pessoais."),
            ("Como confirma se um site de compras é fiável?", ["Tem muitas cores", "Usa HTTPS, tem contactos reais e boas avaliações", "Tem preços muito baixos", "Foi partilhado num grupo"], 1, "Preços demasiado baixos são isco habitual.", "Pesquise o nome da loja + 'burla' antes de comprar."),
        ]),
        ("wifi", "Segurança das redes Wi-Fi", "📶", "#1ABC9C", [
            ("Qual é o maior risco numa rede Wi-Fi pública aberta?", ["Gastar bateria", "Alguém intercetar o que envia", "O sinal ser fraco", "Nenhum"], 1, "Outras pessoas podem observar o tráfego ou criar redes falsas.", "Evite o banco em Wi-Fi público. Use dados móveis."),
            ("Qual segurança Wi-Fi é mais recomendada em casa?", ["Sem senha", "WEP", "WPA2 ou WPA3", "Qualquer um"], 2, "WPA2 e WPA3 são os padrões actuais. WEP é fácil de quebrar.", "No router, use WPA2/WPA3 com senha longa."),
            ("O que deve fazer à senha original do router?", ["Mantê-la", "Alterá-la logo na instalação", "Colá-la no router", "Partilhá-la"], 1, "Senhas de fábrica seguem padrões conhecidos.", "Mude a senha do Wi-Fi e do router."),
            ("Existem duas redes com nomes quase iguais num café. Como agir?", ["Ligar à mais forte", "Perguntar qual é a rede oficial", "Ligar às duas", "Ligar à sem senha"], 1, "Redes falsas com nomes parecidos roubam dados.", "Confirme o nome exacto com o responsável."),
            ("Desligar Wi-Fi e Bluetooth quando não usa ajuda a...", ["Nada", "Reduzir exposição a ligações indesejadas", "Aumentar velocidade", "Apagar vírus"], 1, "Ligações automáticas podem ligar a redes inseguras.", "Desactive a ligação automática a redes abertas."),
        ]),
        ("contas", "Protecção de contas", "🔑", "#F39C12", [
            ("Qual destas é a senha mais forte?", ["123456", "dionisio2005", "Tr0nc0-Azul-Chuva-47!", "senha"], 2, "Senhas longas com várias palavras e símbolos são mais difíceis.", "Use senhas com 12+ caracteres."),
            ("Pode usar a mesma senha em várias contas?", ["Sim, é mais fácil", "Não, se uma for roubada as outras ficam expostas", "Só em redes sociais", "Só no e-mail"], 1, "Atacantes testam a mesma senha noutros sites.", "Use uma senha diferente por conta."),
            ("O que é a autenticação em dois passos (2FA)?", ["Digitar a senha duas vezes", "Um segundo passo além da senha", "Ter duas contas", "Mudar a senha todos os dias"], 1, "Mesmo com a senha roubada, falta o segundo factor.", "Active o 2FA no e-mail, WhatsApp e banco."),
            ("Onde deve guardar as suas senhas?", ["Num papel no ecrã", "Numa nota sem protecção", "Num gestor de senhas", "Num grupo de WhatsApp"], 2, "Gestores cifram os dados e geram senhas únicas.", "Evite guardar senhas em locais visíveis."),
            ("Suspeita que a conta foi invadida. Primeiro passo?", ["Esperar", "Mudar a senha e terminar sessões abertas", "Apagar a conta", "Avisar amanhã"], 1, "Mudar a senha corta o acesso do atacante.", "Verifique também o e-mail e número de recuperação."),
        ]),
    ]
    temas = []
    for id_t, nome, ico, cor, qs in dados:
        perguntas = [Pergunta(*q) for q in qs]
        temas.append(Tema(id_t, nome, ico, cor, perguntas))
    return temas

TEMAS = carregar_temas()

# ---------------- GESTÃO DE HISTÓRICO (JSON) ----------------

class GestorHistorico:
    """Responsável por carregar e guardar o histórico. Tratamento de exceções incluído."""
    @staticmethod
    def carregar():
        try:
            with open(FICHEIRO_HISTORICO, encoding="utf-8") as f:
                dados = json.load(f)
                if not isinstance(dados, dict):
                    return {}
                return dados
        except (OSError, ValueError, json.JSONDecodeError):
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

# ---------------- INTERFACE GRÁFICA ----------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ciber Seguro - UNISAVE")
        self.root.geometry("520x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#2C3E50")
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
        d = GestorHistorico.carregar()
        tk.Label(self.root, text="🛡️ CIBER SEGURO", font=("Helvetica", 22, "bold"), fg="white", bg="#2C3E50").pack(pady=15)
        tk.Label(self.root, text="UNISAVE • Aprenda a proteger-se de burlas e vírus", font=("Helvetica", 10), fg="#BDC3C7", bg="#2C3E50").pack()
        tk.Label(self.root, text="Escolha um tema para começar:", font=("Helvetica", 12, "bold"), fg="#F1C40F", bg="#2C3E50").pack(pady=15)
        for t in TEMAS:
            b = d.get(t.id, {}).get("melhor")
            extra = f"  • Melhor: {b}/5" if b is not None else ""
            tk.Button(self.root, text=f"{t.icone}  {t.nome}{extra}", font=("Helvetica", 12, "bold"), bg=t.cor, fg="white", width=38, height=2, command=lambda tema=t: self.comecar(tema)).pack(pady=5)
        tk.Button(self.root, text="📊 Ver Histórico", font=("Helvetica", 11), bg="#34495E", fg="white", width=38, command=self.mostrar_historico).pack(pady=(15,5))
        tk.Button(self.root, text="❌ Sair", font=("Helvetica", 11), bg="#E74C3C", fg="white", width=38, command=self.root.quit).pack(pady=5)

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
        tk.Label(self.root, text=f"{self.tema.icone} {self.tema.nome}  •  Pergunta {self.idx+1}/{len(self.perguntas)}", font=("Helvetica", 10, "bold"), fg="#F1C40F", bg="#2C3E50").pack(pady=15)
        tk.Label(self.root, text=f"Pontos: {self.pontos}", font=("Helvetica", 11), fg="white", bg="#2C3E50").pack()
        tk.Label(self.root, text=q.texto, font=("Helvetica", 14, "bold"), fg="white", bg="#2C3E50", wraplength=460, justify="center").pack(pady=25, padx=20)
        ordem = list(range(len(q.opcoes)))
        random.shuffle(ordem)
        self.ordem_atual = ordem
        self.pergunta_atual = q
        letras = "ABCD"
        for k, orig in enumerate(ordem):
            tk.Button(self.root, text=f"{letras[k]})  {q.opcoes[orig]}", font=("Helvetica", 11), bg="white", fg="#2C3E50", width=42, height=2, wraplength=380, anchor="w", command=lambda o=orig: self.responder(o)).pack(pady=4)
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
        tk.Label(self.root, text="🏁 RESULTADO", font=("Helvetica", 20, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
        tk.Label(self.root, text=f"{self.pontos}/{total}  •  {perc}%", font=("Helvetica", 28, "bold"), fg="#F1C40F", bg="#2C3E50").pack()
        msg = "🎉 Perfeito! És um expert!" if perc == 100 else "👍 Bom! Revê as recomendações." if perc >= 60 else "⚠️ Precisas de ter mais cuidado online."
        tk.Label(self.root, text=msg, font=("Helvetica", 12), fg="white", bg="#2C3E50").pack(pady=10)
        if self.erradas:
            tk.Label(self.root, text="📌 Recomendações para ti:", font=("Helvetica", 12, "bold"), fg="#F1C40F", bg="#2C3E50").pack(pady=(15,5))
            for q in self.erradas:
                tk.Label(self.root, text=f"• {q.recomendacao}", font=("Helvetica", 10), fg="white", bg="#2C3E50", wraplength=440, justify="left").pack(pady=2, padx=20, anchor="w")
        GestorHistorico.registar(self.tema.id, self.pontos, total)
        tk.Button(self.root, text="🔄 Jogar Novamente", font=("Helvetica", 12, "bold"), bg="#1ABC9C", fg="white", width=30, command=lambda: self.comecar(self.tema)).pack(pady=(20,5))
        tk.Button(self.root, text="🏠 Menu Principal", font=("Helvetica", 11), bg="#34495E", fg="white", width=30, command=self.mostrar_menu).pack(pady=5)

    def mostrar_historico(self):
        self.limpar()
        d = GestorHistorico.carregar()
        tk.Label(self.root, text="📊 HISTÓRICO", font=("Helvetica", 20, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
        if not d:
            tk.Label(self.root, text="Ainda não fizeste nenhum quiz.", font=("Helvetica", 12), fg="#BDC3C7", bg="#2C3E50").pack(pady=20)
        else:
            for t in TEMAS:
                e = d.get(t.id)
                if e:
                    ult = ", ".join(f"{l['s']}/{l['t']} ({l['d']})" for l in e["log"][:3])
                    tk.Label(self.root, text=f"{t.icone} {t.nome}", font=("Helvetica", 12, "bold"), fg="#F1C40F", bg="#2C3E50").pack(pady=(10,0), padx=30, anchor="w")
                    tk.Label(self.root, text=f"Melhor: {e['melhor']}/5  •  Tentativas: {e['tentativas']}\nÚltimos: {ult}", font=("Helvetica", 11), fg="white", bg="#2C3E50", justify="left").pack(padx=30, anchor="w")
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