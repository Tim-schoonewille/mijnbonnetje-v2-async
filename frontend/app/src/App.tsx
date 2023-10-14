import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import NavBar from "./components/navigation/NavBar";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import VerifyEmailPage from "./pages/auth/VerifyEmailPage";
import RequestNewPasswordPage from "./pages/auth/RequestNewPasswordPage";
import RequestNewEmailVerificationPage from "./pages/auth/RequestNewEmailVerificationPage";
import LogoutPage from "./pages/auth/LogoutPage";
import VerifyNewPasswordPage from "./pages/auth/VerifyNewPasswordPage";
import ReceiptsPage from "./pages/receipt/ReceiptsPage";
import AddReceiptPage from "./pages/receipt/AddReceiptPage";
import SingleReceiptPage from "./pages/receipt/SingleReceiptPage";
import AuthProvider from "./context/AuthContext";
import DashboardPage from "./pages/DashboardPage";

export const App = () => {
  return (
    <AuthProvider>
      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />

          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/register" element={<RegisterPage />} />
          <Route path="/auth/logout" element={<LogoutPage />} />
          <Route path="/auth/verify-email" element={<VerifyEmailPage />} />
          <Route
            path="/auth/request-new-password"
            element={<RequestNewPasswordPage />}
          />
          <Route
            path="/auth/verify-new-password"
            element={<VerifyNewPasswordPage />}
          />
          <Route
            path="/auth/request-new-email-verification"
            element={<RequestNewEmailVerificationPage />}
          />

          <Route path="/receipts" element={<ReceiptsPage />} />
          <Route path="/receipts/:id" element={<SingleReceiptPage />} />
          <Route path="/add-receipt" element={<AddReceiptPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};
