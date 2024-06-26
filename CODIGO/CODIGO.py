import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QTableWidgetItem, QTableWidget, QDialog, QFormLayout, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sqlite3

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CRUD COM PYQT E SQLITE')
        self.setGeometry(100, 100, 800, 600)
        self.conexao = sqlite3.connect('database.db')
        self.criar_tabela()
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)
        titulo_label = QLabel('CADASTRO DE CLIENTES', self)
        titulo_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo_label)
        botoes_layout = QHBoxLayout()

        self.botao_adicionar = QPushButton('ADICIONAR', self)
        self.botao_adicionar.clicked.connect(self.abrir_janela_adicionar)
        botoes_layout.addWidget(self.botao_adicionar)

        self.botao_editar = QPushButton('EDITAR', self)
        self.botao_editar.clicked.connect(self.editar_registro)
        botoes_layout.addWidget(self.botao_editar)

        self.botao_deletar = QPushButton('APAGAR', self)
        self.botao_deletar.clicked.connect(self.deletar_registro)
        botoes_layout.addWidget(self.botao_deletar)

        layout_principal.addLayout(botoes_layout)
        self.tabela_clientes = QTableWidget(self)
        self.tabela_clientes.setColumnCount(4)
        self.tabela_clientes.setHorizontalHeaderLabels(['ID', 'NOME', 'EMAIL', 'TELEFONE'])
        layout_principal.addWidget(self.tabela_clientes)
        self.carregar_dados()

    def criar_tabela(self):
        cursor = self.conexao.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nome TEXT,
                          email TEXT,
                          telefone TEXT
                          )''')
        self.conexao.commit()

    def carregar_dados(self):
        self.tabela_clientes.setRowCount(0)
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM clientes')
        dados = cursor.fetchall()
        for row_number, row_data in enumerate(dados):
            self.tabela_clientes.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tabela_clientes.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def abrir_janela_adicionar(self):
        dialog = DialogoAdicionar(self)
        if dialog.exec_() == QDialog.Accepted:
            nome = dialog.nome.text()
            email = dialog.email.text()
            telefone = dialog.telefone.text()
            self.inserir_registro(nome, email, telefone)

    def inserir_registro(self, nome, email, telefone):
        cursor = self.conexao.cursor()
        cursor.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
        self.conexao.commit()
        self.carregar_dados()

    def editar_registro(self):
        if self.tabela_clientes.selectedItems():
            selected_row = self.tabela_clientes.currentRow()
            id = self.tabela_clientes.item(selected_row, 0).text()
            nome = self.tabela_clientes.item(selected_row, 1).text()
            email = self.tabela_clientes.item(selected_row, 2).text()
            telefone = self.tabela_clientes.item(selected_row, 3).text()
            dialog = DialogoEditar(self, id, nome, email, telefone)
            if dialog.exec_() == QDialog.Accepted:
                novo_nome = dialog.nome.text()
                novo_email = dialog.email.text()
                novo_telefone = dialog.telefone.text()
                self.atualizar_registro(id, novo_nome, novo_email, novo_telefone)

    def atualizar_registro(self, id, nome, email, telefone):
        cursor = self.conexao.cursor()
        cursor.execute('UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?', (nome, email, telefone, id))
        self.conexao.commit()
        self.carregar_dados()

    def deletar_registro(self):
        if self.tabela_clientes.selectedItems():
            selected_row = self.tabela_clientes.currentRow()
            id = self.tabela_clientes.item(selected_row, 0).text()
            mensagem_box = QMessageBox(QMessageBox.Question, 'Confirmar Exclusão', 'Tem certeza que deseja excluir este registro?', QMessageBox.Yes | QMessageBox.No, self)
            if mensagem_box.exec_() == QMessageBox.Yes:
                cursor = self.conexao.cursor()
                cursor.execute('DELETE FROM clientes WHERE id=?', (id,))
                self.conexao.commit()
                self.carregar_dados()

    def closeEvent(self, event):
        self.conexao.close()
        event.accept()

class DialogoAdicionar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('ADICIONAR CLIENTE')
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.nome = QLineEdit(self)
        self.nome.setPlaceholderText('NOME')
        layout.addWidget(self.nome)

        self.email = QLineEdit(self)
        self.email.setPlaceholderText('EMAIL')
        layout.addWidget(self.email)

        self.telefone = QLineEdit(self)
        self.telefone.setPlaceholderText('TELEFONE')
        layout.addWidget(self.telefone)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)
        layout.addWidget(botoes)

class DialogoEditar(DialogoAdicionar):
    def __init__(self, parent=None, id='', nome='', email='', telefone=''):
        super().__init__(parent)

        self.setWindowTitle('EDITAR CLIENTE')
        self.setModal(True)

        self.id = id
        self.nome.setText(nome)
        self.email.setText(email)
        self.telefone.setText(telefone)

    def accept(self):
        super().accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
