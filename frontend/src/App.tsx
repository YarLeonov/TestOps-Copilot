import { Route, Routes } from "react-router-dom";
import Layout from "./components/layout/Layout";
import Home from "./pages/Home";
import ScenarioUI from "./pages/ScenarioUI";
import ScenarioAPI from "./pages/ScenarioAPI";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ui" element={<ScenarioUI />} />
        <Route path="/api" element={<ScenarioAPI />} />
      </Routes>
    </Layout>
  );
}

export default App;
