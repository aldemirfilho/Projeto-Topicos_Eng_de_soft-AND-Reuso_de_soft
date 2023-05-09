import streamlit as st


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def to_dict(self):
        return {"name": self.name, "email": self.email, "password": self.password}
    
    @staticmethod
    def from_dict(user_dict):
        return User(user_dict["name"], user_dict["email"], user_dict["password"])
    
    def __repr__(self):
        return f"User(name='{self.name}', email='{self.email}', password='{self.password}')"


    def register_user(users, form_submitted):

        submit_button = False
        with st.form(key="register_form") :
            st.subheader("Registrar novo usuário")
            name = st.text_input("Nome")
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirme a senha", type="password")
            col1, col2 = st.columns([1, 13])
            submit_button = col1.form_submit_button(label="Registrar")
            ok_button = col2.form_submit_button(label="Ok")
            if submit_button: 
                for user in users:
                    if user["email"] == email:
                        st.error("Usuário já existe!")
                        return users, form_submitted

                if password == confirm_password:
                    user = User(name, email, password)
                    users.append(user.to_dict())
                    st.success("Usuário registrado com sucesso! Prossiga para a tela inicial apertando o botão 'Ok'")

                else:
                    st.error("As senhas não coincidem!")
            if ok_button:
                form_submitted = True
        
        return users, form_submitted    
        


    def login_user(users, logged_in):
        with st.form(key="login_form"):
            st.subheader("Login")
            email = st.text_input("E-mail")
            password = st.text_input("Senha", type="password")
            col1, col2 = st.columns([1, 13])
            submit_button = col1.form_submit_button(label="Entrar")
            ok_button = col2.form_submit_button(label="Ok")
            if submit_button:
                for user in users:
                    if user["email"] == email and user["password"] == password:
                        st.success("Login realizado com sucesso! Click em 'Ok' para prosseguir")
                        logged_in = True
                        if ok_button:
                            return logged_in
                        
                    else:
                        st.error("E-mail ou senha incorretos!")
        return logged_in