import React from "react";

export default function UserInfo({userData}) {
    const logOut = () => {
        window.localStorage.clear();
        window.location.href = "/login";
    };
    return (<div>
        ID<h1>{userData.id}</h1> Логин <h1>{userData.username}</h1>
        <br/>
        <button onClick={logOut} className="btn btn-primary">
            Выйти
        </button>
    </div>);
}
