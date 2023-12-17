import React, {useState} from "react";
import {apiUrl} from "../config";

export default function SignUp() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`${apiUrl}/api/auth/`, {
            method: "POST", crossDomain: true, headers: {
                "content-Type": "application/json", "accept": "application/json", "access-Control-Allow-Origin": "*",
            }, body: JSON.stringify({
                username, password,
            }),
        })

        if (!response.ok) {
            alert("Что-то пошло не так");
            return
        }

        window.location.href = "./login";
    };

    return (<div className="auth-wrapper">
        <div className="auth-inner">
            <form onSubmit={handleSubmit}>
                <h3>Регистрация</h3>

                <div className="mb-3">
                    <label>Логин</label>
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Введи логин"
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="mb-3">
                    <label>Пароль</label>
                    <input
                        type="password"
                        className="form-control"
                        placeholder="Введи пароль"
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div className="d-grid">
                    <button type="submit" className="btn btn-primary">
                        Зарегистрироваться
                    </button>
                </div>
                <p className="forgot-password text-right">
                    Уже зарегистрированы? <a href="/login">Войти</a>
                </p>
            </form>
        </div>
    </div>);
}
