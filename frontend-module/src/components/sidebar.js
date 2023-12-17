import React from "react";
import {Link} from "react-router-dom";
import '../styles/sidebar.css'


const Sidebar = () => {
    return (
        <div className="sidebar m-3">
            <div className="sidebar-links">
                <Link to="/dashboard/">Обо мне</Link>
                <Link to="/dashboard/client">Мои клиенты</Link>
                <Link to="/dashboard/chat">Генерация предложений</Link>
                <Link to="/dashboard/chat/history">История генераций</Link>
            </div>
        </div>
    );
};

export default Sidebar;

const sidebarNavItems = [
    {
        display: 'Обо мне',
        to: '/dashboard',
        section: ''
    },
    {
        display: 'Мои клиенты',
        to: '/dashboard/client',
        section: ''
    },
    {
        display: 'Генерация предложений',
        to: '/dashboard/chat',
        section: ''
    },
];
