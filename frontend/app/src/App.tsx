import * as React from "react";
import { ChakraProvider, theme } from "@chakra-ui/react";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Logo } from "./Logo";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./Home";
import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AuthProvider, { useAuthContext } from "./context/AuthContext";
import LogoutPage from "./pages/LogoutPage";
import AddReceiptPage from "./pages/AddReceiptPage";
import ReceiptsPage from "./pages/ReceiptsPage";
import VerifyEmailPage from "./pages/VerifyEmailPage";
import SingleReceiptPage from "./pages/SingleReceiptPage";

export const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <AuthProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/receipts" element={<ReceiptsPage />} />
            <Route path="/receipts/:id" element={<SingleReceiptPage />} />
            <Route path="/addreceipt" element={<AddReceiptPage />} />
            <Route path="/auth/login" element={<LoginPage />} />
            <Route path="/auth/logout" element={<LogoutPage />} />
            <Route path="/auth/register" element={<RegisterPage />} />
            <Route path="/auth/verify-email" element={<VerifyEmailPage />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ChakraProvider>
  );
};
