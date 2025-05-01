import './chatBot.css';
import React, { useEffect, useState } from 'react';
import { IoMdSend } from 'react-icons/io';
import { BiBot, BiUser } from 'react-icons/bi';

function Basic() {
    const [chat, setChat] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [botTyping, setbotTyping] = useState(false);

    useEffect(() => {
        const objDiv = document.getElementById('messageArea');
        objDiv.scrollTop = objDiv.scrollHeight;
    }, [chat]);

    const handleSubmit = (evt) => {
        evt.preventDefault();
        const name = "shreyas";
        const request_temp = { sender: "user", sender_id: name, msg: inputMessage };

        if (inputMessage !== "") {
            setChat(chat => [...chat, request_temp]);
            setbotTyping(true);
            setInputMessage('');
            rasaAPI(name, inputMessage);
        } else {
            window.alert("Please enter valid message");
        }
    };

    const rasaAPI = async function handleClick(name, msg) {
        try {
            const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'charset': 'UTF-8',
                },
                credentials: "same-origin",
                body: JSON.stringify({ "sender": name, "message": msg }),
            });
            const data = await response.json();

            if (data && data.length > 0) {
                const temp = data[0];
                const recipient_id = temp["recipient_id"];
                const recipient_msg = temp["text"];

                const response_temp = { sender: "bot", recipient_id: recipient_id, msg: recipient_msg };
                setbotTyping(false);

                setChat(chat => [...chat, response_temp]);
            } else {
                setbotTyping(false);
                setChat(chat => [...chat, { sender: "bot", msg: "Sorry, I didn't understand that." }]);
            }
        } catch (error) {
            console.error("Error contacting Rasa API:", error);
            setbotTyping(false);
            setChat(chat => [...chat, { sender: "bot", msg: "Sorry, there was an error. Please try again." }]);
        }
    };

    return (
        <div>
            <div className="container">
                <div className="row justify-content-center">
                    <div className="card" style={{ maxWidth: '35rem', border: '1px solid black', paddingLeft: '0px', paddingRight: '0px', borderRadius: '30px', boxShadow: '0 16px 20px 0 rgba(0,0,0,0.4)' }}>
                        <div className="cardHeader text-white" style={{ height: '4.5rem', borderBottom: '1px solid black', borderRadius: '30px 30px 0px 0px', backgroundColor: '#8012c4' }}>
                            <h1 style={{ marginBottom: '0px' }}>AI Assistant</h1>
                            {botTyping ? <h6>Bot Typing....</h6> : null}
                        </div>
                        <div className="cardBody" id="messageArea" style={{ paddingTop: '10px', height: '28rem', overflowY: 'auto', overflowX: 'hidden' }}>
                            <div className="row msgarea">
                                {chat.map((user, key) => (
                                    <div key={key}>
                                        {user.sender === 'bot' ?
                                            <div className='msgalignstart'>
                                                <BiBot className="botIcon" />
                                                <h5 className="botmsg">{user.msg}</h5>
                                            </div>
                                            :
                                            <div className='msgalignend'>
                                                <h5 className="usermsg">{user.msg}</h5>
                                                <BiUser className="userIcon" />
                                            </div>
                                        }
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="cardFooter text-white" style={{ borderTop: '1px solid black', borderRadius: '0px 0px 30px 30px', backgroundColor: '#8012c4' }}>
                            <div className="row">
                                <form style={{ display: 'flex' }} onSubmit={handleSubmit}>
                                    <div className="col-10" style={{ paddingRight: '0px' }}>
                                        <input onChange={e => setInputMessage(e.target.value)} value={inputMessage} type="text" className="msginp" />
                                    </div>
                                    <div className="col-2 cola">
                                        <button type="submit" className="circleBtn"><IoMdSend className="sendBtn" /></button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Basic;
