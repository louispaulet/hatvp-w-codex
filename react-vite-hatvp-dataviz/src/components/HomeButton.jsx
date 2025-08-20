import Button from '@mui/material/Button';
import HomeIcon from '@mui/icons-material/Home';
import { Link as RouterLink } from 'react-router-dom';

function HomeButton({ label = 'Back to Home', variant = 'text', size = 'small', sx = {}, ...props }) {
  return (
    <Button
      component={RouterLink}
      to="/"
      variant={variant}
      size={size}
      startIcon={<HomeIcon />}
      sx={{ textTransform: 'none', ...sx }}
      {...props}
    >
      {label}
    </Button>
  );
}

export default HomeButton;

