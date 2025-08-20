import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Box from '@mui/material/Box';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import OrganizationMentions from './pages/OrganizationMentions';
import DelayByMandate from './pages/DelayByMandate';
import About from './pages/About';
import Demographics from './pages/Demographics';

function App() {
  return (
    <BrowserRouter>
      <Box display="flex" flexDirection="column" minHeight="100vh">
        <NavBar />
        <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
          <Routes>
            <Route path="/" element={<OrganizationMentions />} />
            <Route path="/demographics" element={<Demographics />} />
            <Route path="/delay" element={<DelayByMandate />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Box>
        <Footer />
      </Box>
    </BrowserRouter>
  );
}

export default App;
