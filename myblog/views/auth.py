from flask import ( 
    render_template, #renderiza el template de las vistas
    Blueprint, # registra las vistas en la app
    flash, # Para lanzar mensajes de error
    g, # Usuario en secion
    redirect, # redireccionar a una nueva ruta
    request, # capturar la peticion del cliente
    session, # para consultar la bd
    url_for, #redirecciona a otra ruta
)

from werkzeug.security import check_password_hash, generate_password_hash

from myblog.models.user import User

from myblog import db

from os import error

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Registro de ususario

@auth.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username, generate_password_hash(password)) # Objeto

        error = None
        if not username:
            error = 'Se requiere nombre de usuario'
        elif not password:
            error = 'Se requiere una contraseña'
        
        #pata filtrar los nombres registrados
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit() #Para el cambio
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
        flash(error) #muestra el mensaje de error

    return render_template('auth/register.html')

# iniciar Sesion

@auth.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        
        user = User.query.filter_by(username = username).first()

        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña invalida'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))
        flash(error)

    return render_template('auth/login.html')

#logear el usuario
@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

# Para cerrar sesion
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

#para poder visualizar algunos parametros de al pagina
import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view