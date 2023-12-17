import React, {useState} from "react";
import {Button, Form, ListGroup, Pagination, Stack} from "react-bootstrap";

const ChatHistory = ({infChannels, products, chats}) => {
    const [messages, setMessages] = useState([]);
    const [pageMessages, setPageMessages] = useState([]);
    const [active, setActive] = useState(1);
    const [inputClientId, setInputClientId] = useState(0);

    const getItems = () => {
        const items = [];
        const pages = Math.floor((messages.length - 1) / 10 + 1);
        for (let number = 1; number <= pages; number++) {
            items.push(<Pagination.Item key={number} active={number === active} onClick={() => setActivePage(number)}>
                {number}
            </Pagination.Item>)
        }
        return items
    }

    const getChatByClientId = (clientId) => {
        const messagesTemp = [];
        const pageMessagesTemp = [];

        chats.map((chat, i) => {
            if (chat.client_id === clientId) {
                const question = {
                    sender: "user",
                    text: "Название продукта: "+products[chat.product_id-1].title+", Канал коммуникации: "+infChannels[chat.channel_id-1].name
                };
                const answer = {
                    sender: "bot",
                    text: chats[i+1].text
                };
                messagesTemp.push(question, answer);
            }
        });

        const messagesSlice = messagesTemp.slice(0, messagesTemp.length >= 10 ? 10 : messagesTemp.length%10);
        messagesSlice.map(val => {
            pageMessagesTemp.push(val);
        })

        setMessages(messagesTemp);
        setPageMessages(pageMessagesTemp);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        getChatByClientId(inputClientId);

        setInputClientId(0);
    };

    const setActivePage = (number) => {
        const pageMessagesTemp = [];

        const messagesSlice = messages.slice((number-1)*10, number*10 > messages.length ? messages.length : number*10);
        messagesSlice.map(val => {
            pageMessagesTemp.push(val);
        })

        setActive(number);
        setPageMessages(pageMessagesTemp);
    }

    return (
        <div className="chat-container">
            <Form onSubmit={handleSubmit} className="message-input">
                <Form.Group controlId="clientId">
                    <Form.Label>ID Клиента</Form.Label>
                    <Form.Control
                        type="number"
                        placeholder="Введите идентификатор клиента"
                        value={inputClientId}
                        onChange={(e) => setInputClientId(e.target.valueAsNumber)}
                    />
                </Form.Group>
                <Button variant="primary" type="submit" disabled={!inputClientId}>
                    Отправить
                </Button>
            </Form>

            <Stack gap={3}>
                <ListGroup className="message-list">
                    {pageMessages.map((message, index) => (
                        <ListGroup.Item key={index} className={`message ${message.sender}`}>
                            {message.text}
                        </ListGroup.Item>
                    ))}
                </ListGroup>
                {
                    messages.length !== 0 ?
                        <Pagination>
                            <Pagination.First onClick={() => setActivePage(1)}/>
                            <Pagination.Prev disabled={active === 1} onClick={() => setActivePage(active - 1)}/>
                            {getItems()}
                            <Pagination.Next disabled={active === Math.floor((messages.length - 1) / 10 + 1)}
                                             onClick={() => setActivePage(active + 1)}/>
                            <Pagination.Last onClick={() => setActivePage(Math.floor((messages.length - 1) / 10 + 1))}/>
                        </Pagination>
                        : <></>
                }
            </Stack>
        </div>
    );
};

export default ChatHistory;