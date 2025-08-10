import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

function Footer() {
  return (
    <Box component="footer" sx={{ mt: 6, py: 3, bgcolor: 'background.paper', borderTop: '1px solid', borderColor: 'divider' }}>
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          Data from HATVP open datasets.
        </Typography>
      </Container>
    </Box>
  );
}

export default Footer;
