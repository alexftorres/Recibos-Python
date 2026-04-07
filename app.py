from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User, Recibo
import hashlib
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def index():
        if 'iduser' in session:
            return redirect(url_for('generate'))
        return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            login_input = request.form.get('login')
            senha = hashlib.md5(request.form.get('senha').encode()).hexdigest()
            user = User.query.filter_by(loginuser=login_input, passworduser=senha).first()
            if user:
                session['iduser'] = user.iduser
                return redirect(url_for('index'))
            else:
                flash('E-mail ou senha inválidos', 'danger')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            nome = request.form.get('nome')
            login = request.form.get('login')
            senha = hashlib.md5(request.form.get('senha').encode()).hexdigest()
            senha2 = hashlib.md5(request.form.get('senha2').encode()).hexdigest()
            if senha == senha2:
                new_user = User(nameuser=nome, loginuser=login, passworduser=senha)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash('As senhas digitadas não estão iguais', 'danger')
        return render_template('register.html')

    @app.route('/generate', methods=['GET', 'POST'])
    def generate():
        if 'iduser' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            valor_str = request.form.get('valor')
            valor = float(valor_str.replace(',', '.'))
            data = request.form.get('data')
            pagador = request.form.get('pagador')
            docpag = request.form.get('docpagador')
            referente = request.form.get('referencia')
            recebedor = request.form.get('recebedor')
            docreceb = request.form.get('docrecebedor')
            fonereceb = request.form.get('fonerecebedor')
            iduser = session['iduser']
            new_recibo = Recibo(
                valorRecibo=valor,
                dataRecibo=datetime.strptime(data, '%Y-%m-%d').date(),
                pagadorRecibo=pagador,
                docPagRecibo=docpag,
                campoRefRecibo=referente,
                recebedorRecibo=recebedor,
                docRecebRecibo=docreceb,
                foneRecebRecibo=fonereceb,
                iduser=iduser
            )
            db.session.add(new_recibo)
            db.session.commit()
            return redirect(url_for('receipt'))
        return render_template('generate.html', recebedor_default=app.config['RECEBEDOR_DEFAULT'], cpf_recebedor_default=app.config['CPF_RECEBEDOR_DEFAULT'], telefone_recebedor_default=app.config['TELEFONE_RECEBEDOR_DEFAULT'])

    @app.route('/receipt')
    def receipt():
        if 'iduser' not in session:
            return redirect(url_for('login'))
        iduser = session['iduser']
        recibo = Recibo.query.filter_by(iduser=iduser).order_by(Recibo.idrecibo.desc()).first()
        if not recibo:
            return redirect(url_for('generate'))
        # Process data like original
        valor = f"{recibo.valorRecibo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        dia = recibo.dataRecibo.weekday() + 1  # Monday=0, so +1
        mes = recibo.dataRecibo.month
        data_recibo = f"{dias_semana[dia-1]}, {recibo.dataRecibo.day} de {meses[mes]} de {recibo.dataRecibo.year}"
        return render_template('receipt.html', recibo=recibo, valor=valor, datarecibo=data_recibo)

    @app.route('/my_receipts')
    def my_receipts():
        if 'iduser' not in session:
            return redirect(url_for('login'))
        iduser = session['iduser']
        recibos = Recibo.query.filter_by(iduser=iduser).all()
        for recibo in recibos:
            recibo.formatted_valor = f"{recibo.valorRecibo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return render_template('my_receipts.html', recibos=recibos)

    @app.route('/reprint/<int:idrecibo>')
    def reprint(idrecibo):
        if 'iduser' not in session:
            return redirect(url_for('login'))
        recibo = Recibo.query.filter_by(idrecibo=idrecibo, iduser=session['iduser']).first()
        if not recibo:
            return redirect(url_for('my_receipts'))
        # Same processing as receipt
        valor = f"{recibo.valorRecibo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        dia = recibo.dataRecibo.weekday() + 1
        mes = recibo.dataRecibo.month
        data_recibo = f"{dias_semana[dia-1]}, {recibo.dataRecibo.day} de {meses[mes]} de {recibo.dataRecibo.year}"
        return render_template('receipt.html', recibo=recibo, valor=valor, datarecibo=data_recibo)

    @app.route('/config', methods=['GET', 'POST'])
    def config():
        if 'iduser' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            recebedor = request.form.get('recebedor')
            cpf = request.form.get('cpf')
            telefone = request.form.get('telefone')
            # Update .env
            env_path = '.env'
            with open(env_path, 'r') as f:
                lines = f.readlines()
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('RECEBEDOR_DEFAULT='):
                        f.write(f'RECEBEDOR_DEFAULT={recebedor}\n')
                    elif line.startswith('CPF_RECEBEDOR_DEFAULT='):
                        f.write(f'CPF_RECEBEDOR_DEFAULT={cpf}\n')
                    elif line.startswith('TELEFONE_RECEBEDOR_DEFAULT='):
                        f.write(f'TELEFONE_RECEBEDOR_DEFAULT={telefone}\n')
                    else:
                        f.write(line)
            flash('Configurações salvas com sucesso!', 'success')
            return redirect(url_for('config'))
        return render_template('config.html', recebedor_default=app.config['RECEBEDOR_DEFAULT'], cpf_recebedor_default=app.config['CPF_RECEBEDOR_DEFAULT'], telefone_recebedor_default=app.config['TELEFONE_RECEBEDOR_DEFAULT'])

    @app.route('/logout')
    def logout():
        session.pop('iduser', None)
        return redirect(url_for('login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)