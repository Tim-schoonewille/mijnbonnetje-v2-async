import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import NavBar from "./components/navigation/NavBar";

export const App = () => {
  return (
    <>

      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </Router>
    </>
  );
};
