import React, {useState} from "react";
import {apiUrl} from '../config'

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();

        const response = await fetch(`${apiUrl}/api/auth/login`, {
            method: "POST", crossDomain: true, headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Access-Control-Allow-Origin": "*"
            }, body: new URLSearchParams({
                'username': username, 'password': password, 'grant_type': 'password'
            })
        });

        if (!response.ok) {
            alert('Что-то пошло не так')
            return
        }

        const data = await response.json()

        console.log(data, "userRegister")
        window.localStorage.setItem("token", data.access_token);
        window.localStorage.setItem("loggedIn", true);

        window.location.href = "./dashboard";
    }

    return (<div className="auth-wrapper">
        <div className="auth-inner">
            <form onSubmit={handleSubmit}>
                <h3>Вход</h3>

                <div className="mb-3">
                    <label>Логин</label>
                    <input
                        type="username"
                        className="form-control"
                        placeholder="Введи свой логин"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="mb-3">
                    <label>Пароль</label>
                    <input
                        type="password"
                        className="form-control"
                        placeholder="********"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div className="mb-3">
                    <div className="custom-control custom-checkbox">
                        <input
                            type="checkbox"
                            className="custom-control-input"
                            id="customCheck1"
                        />
                        <label className="custom-control-label" htmlFor="customCheck1">
                            Запомнить меня
                        </label>
                    </div>
                </div>

                <div className="d-grid">
                    <button type="submit" className="btn btn-primary">
                        Войти
                    </button>
                </div>
                <p className="forgot-password text-right">
                    <a href="/register">Зарегистрироваться</a>
                </p>
            </form>
        </div>
    </div>);
}
