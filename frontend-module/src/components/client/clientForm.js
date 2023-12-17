import React, {useState} from "react";
import '../../styles/createClientForm.css'
import CreateClientForm from "./createClientForm";
import ClientTable from "./clientTable";

const ClientForm = ({clients, fetchClients}) => {
    const [showForm, setShowForm] = useState(false);

    const toggleForm = () => {
        setShowForm(!showForm);
    };

    return (<div>
        <button onClick={toggleForm} className="btn btn-primary mb-3">
            {showForm ? "Спрятать" : "Добавить клиента"}
        </button>

        {showForm && <CreateClientForm fetchClients={fetchClients}/>}

        <ClientTable clients={clients} fetchClients={fetchClients}/>
    </div>);
};

export default ClientForm;
