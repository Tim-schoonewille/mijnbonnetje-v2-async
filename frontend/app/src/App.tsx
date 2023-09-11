import * as React from "react";
import { ChakraProvider, theme } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Logo } from "./Logo";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./Home";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AuthProvider from "./context/AuthContext";
import LogoutPage from "./pages/LogoutPage";

export const App = () => (
  <ChakraProvider theme={theme}>
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
                    <Route path="/logout" element={<LogoutPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  </ChakraProvider>
);
