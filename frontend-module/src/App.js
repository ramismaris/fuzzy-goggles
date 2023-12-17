import React from "react";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import {BrowserRouter as Router, Navigate, Route, Routes} from "react-router-dom";

import Login from "./components/login_component";
import SignUp from "./components/signup_component";
import Dashboard from "./components/dashboard";

function App() {
    const isLoggedIn = window.localStorage.getItem("loggedIn");
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route
                        exact
                        path="/"
                        element={isLoggedIn === "true" ? <Navigate to="/dashboard"/> : <Login/>}
                    />
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<SignUp/>}/>
                    <Route path="/dashboard/*" element={<Dashboard/>}/>
                </Routes>
            </div>
        </Router>
    );
}

export default App;
