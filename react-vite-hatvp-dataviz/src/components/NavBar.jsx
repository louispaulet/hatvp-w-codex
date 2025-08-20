import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { Link as RouterLink, useLocation } from 'react-router-dom';

function NavBar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ mr: 2 }}>
          HATVP Explorer
        </Typography>
        <Button
          color="inherit"
          component={RouterLink}
          to="/"
          variant={isActive('/') ? 'outlined' : 'text'}
          aria-current={isActive('/') ? 'page' : undefined}
        >
          Organizations
        </Button>
        <Button
          color="inherit"
          component={RouterLink}
          to="/demographics"
          variant={isActive('/demographics') ? 'outlined' : 'text'}
          aria-current={isActive('/demographics') ? 'page' : undefined}
        >
          Demographics
        </Button>
        <Button
          color="inherit"
          component={RouterLink}
          to="/delay"
          variant={isActive('/delay') ? 'outlined' : 'text'}
          aria-current={isActive('/delay') ? 'page' : undefined}
        >
          Delays
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        <Button
          color="inherit"
          component={RouterLink}
          to="/about"
          variant={isActive('/about') ? 'outlined' : 'text'}
          aria-current={isActive('/about') ? 'page' : undefined}
        >
          About
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;
