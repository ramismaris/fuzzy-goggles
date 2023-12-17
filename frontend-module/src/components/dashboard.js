import React, {useEffect, useState} from "react";
import {Route, Routes} from "react-router-dom";

import {apiUrl} from "../config";

import UserInfo from "./userInfo";
import Sidebar from "./sidebar";
import ClientForm from "./client/clientForm";
import ChatForm from "./chat/chatForm";

import '../styles/dashboard.css'
import ChatHistory from "./chat/chatHistory";

export default function Dashboard() {
    const [userData, setUserData] = useState("");
    const [clients, setClients] = useState([]);
    const [chats, setChats] = useState([]);
    const [infChannels, setInfChannels] = useState([]);
    const [products, setProducts] = useState([]);

    async function getInfoAboutMe() {
        const response = await fetch(`${apiUrl}/api/auth/`, {
            method: "GET", crossDomain: true, headers: {
                "content-Type": "application/json",
                "accept": "application/json",
                "access-Control-Allow-Origin": "*",
                "authorization": `Bearer ${window.localStorage.getItem("token")}`
            },
        });

        if (!response.ok) {
            alert("Токен истек войдите заново");
            window.localStorage.clear();
            window.location.href = "/login";
            return
        }

        const data = await response.json();
        setUserData(data);
    }

    async function fetchClients() {
        const response = await fetch(`${apiUrl}/api/client/`, {
            method: "GET", headers: {Authorization: `Bearer ${window.localStorage.getItem("token")}`,},
        });

        if (!response.ok) {
            alert("Что-то пошло не так при загрузке клиентов");
            return;
        }

        const data = await response.json();
        setClients(data);
    }

    async function fetchChats() {
        const response = await fetch(`${apiUrl}/api/chat/`, {
            method: "GET", headers: {Authorization: `Bearer ${window.localStorage.getItem("token")}`,},
        });

        if (!response.ok) {
            alert("Что-то пошло не так при загрузке чатов");
            return;
        }

        const data = await response.json();
        setChats(data);
    }

    async function fetchInformationChannels() {
        const response = await fetch(`${apiUrl}/api/information_channel/`, {
            method: "GET", headers: {Authorization: `Bearer ${window.localStorage.getItem("token")}`,},
        });

        if (!response.ok) {
            alert("Что-то пошло не так при загрузке каналов");
            return;
        }

        const data = await response.json();
        setInfChannels(data);
    }

    async function fetchProducts() {
        const response = await fetch(`${apiUrl}/api/product/`, {
            method: "GET", headers: {Authorization: `Bearer ${window.localStorage.getItem("token")}`,},
        });

        if (!response.ok) {
            alert("Что-то пошло не так при загрузке продуктов");
            return;
        }

        const data = await response.json();
        setProducts(data);
    }

    useEffect(() => {
        getInfoAboutMe();
        fetchClients();
        fetchChats();
        fetchInformationChannels();
        fetchProducts();
    }, []);

    return (<div>
        <div className="dashboard-wrapper">
            <div className="dashboard-inner">
                <Sidebar/>
                <Routes>
                    <Route path="/client" element={<ClientForm clients={clients} fetchClients={fetchClients}/>}/>
                    <Route path="/" element={<UserInfo userData={userData}/>}/>
                    <Route path="/chat" element={<ChatForm infChannels={infChannels} products={products}/>}/>
                    <Route path="/chat/history" element={<ChatHistory infChannels={infChannels} products={products} chats={chats}/>}/>
                </Routes>
            </div>
        </div>
    </div>);
}
