import React, {useState} from "react";
import {Button, Form, ListGroup, Pagination, Stack} from "react-bootstrap";
import "../../styles/userChat.css";
import {apiUrl} from "../../config";

const ChatForm = ({infChannels, products}) => {
    const [messages, setMessages] = useState([]);
    const [pageMessages, setPageMessages] = useState([]);
    const [active, setActive] = useState(1);
    const [formData, setFormData] = useState({
        client_id: 0, product_id: 1, channel_id: 1,
    });

    const getItems = () => {
        const items = [];
        const pages = (messages.length - 1) / 10 + 1;
        for (let number = 1; number <= pages; number++) {
            items.push(<Pagination.Item key={number} active={number === active} onClick={() => setActivePage(number)}>
                {number}
            </Pagination.Item>)
        }
        return items
    }

    const setActivePage = (number) => {
        const pageMessagesTemp = [];

        const messagesSlice = messages.slice((number - 1) * 10, number * 10 > messages.length ? messages.length : number * 10);
        messagesSlice.map(val => {
            pageMessagesTemp.push(val);
        })

        setActive(number);
        setPageMessages(pageMessagesTemp);
    }

    const addChat = (chat) => {
        const messagesTemp = messages;
        const pageMessagesTemp = [];

        const question = {
            sender: "user",
            text: "Название продукта: " + products[formData.product_id - 1].title + ", Канал коммуникации: " + infChannels[formData.channel_id - 1].name
        };
        const answer = {
            sender: "bot", text: chat.text
        };
        messagesTemp.push(question, answer);
        const messagesSlice = messagesTemp.slice(0, messagesTemp.length >= 10 ? 10 : messagesTemp.length % 10);
        messagesSlice.map(val => {
            pageMessagesTemp.push(val);
        })

        setMessages(messagesTemp);
        setPageMessages(pageMessagesTemp);
    }

    const handleChange = (e) => {
        setFormData({
            ...formData, [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`${apiUrl}/api/chat`, {
            method: "POST", headers: {
                "content-Type": "application/json", "authorization": `Bearer ${window.localStorage.getItem("token")}`,
            }, body: JSON.stringify(formData),
        });

        if (!response.ok) {
            alert("Что-то пошло не так при отправке данных");
            return;
        }

        const data = await response.json();
        addChat(data);
        setFormData({
            client_id: 0, product_id: 1, channel_id: 1,
        });
    };

    return (<div className="chat-container">
            <Form onSubmit={handleSubmit} className="message-input">
                <Form.Group controlId="clientId">
                    <Form.Label>ID Клиента</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="Введите идентификатор клиента"
                        value={formData.client_id}
                        name="client_id"
                        onChange={handleChange}
                    />
                </Form.Group>
                <Form.Group controlId="productName">
                    <Form.Label>Продукт</Form.Label>
                    <Form.Select
                        aria-label="Продукт"
                        name="product_id"
                        value={formData.product_id}
                        onChange={handleChange}
                    >
                        {products.map(product => {
                            return <option value={product.id}>{product.title}</option>
                        })}
                    </Form.Select>
                </Form.Group>
                <Form.Group controlId="productName">
                    <Form.Label>Канал коммуникации</Form.Label>
                    <Form.Select
                        aria-label="Канал коммуникации"
                        name="channel_id"
                        value={formData.channel_id}
                        onChange={handleChange}
                    >
                        {infChannels.map(chan => {
                            return <option value={chan.id}>{chan.name}</option>
                        })}
                    </Form.Select>
                </Form.Group>
                <Button variant="primary" type="submit" disabled={!formData.client_id && !formData.product_name}>
                    Отправить
                </Button>
            </Form>

            <Stack gap={3}>
                <ListGroup className="message-list">
                    {pageMessages.map((message, index) => (
                        <ListGroup.Item key={index} className={`message ${message.sender}`}>
                            {message.text}
                        </ListGroup.Item>))}
                </ListGroup>
                {messages.length !== 0 ? <Pagination>
                    <Pagination.First onClick={() => setActivePage(1)}/>
                    <Pagination.Prev disabled={active === 1} onClick={() => setActivePage(active - 1)}/>
                    {getItems()}
                    <Pagination.Next disabled={active === Math.floor((messages.length - 1) / 10 + 1)}
                                     onClick={() => setActivePage(active + 1)}/>
                    <Pagination.Last onClick={() => setActivePage(Math.floor((messages.length - 1) / 10 + 1))}/>
                </Pagination> : <></>}
            </Stack>
        </div>);
};

export default ChatForm;
