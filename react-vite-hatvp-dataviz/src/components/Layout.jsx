import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';

export function PageContainer({ children, maxWidth = 'xl', sx = {}, ...props }) {
  return (
    <Container maxWidth={maxWidth} sx={{ py: { xs: 4, md: 6 }, ...sx }} {...props}>
      {children}
    </Container>
  );
}

export function SectionCard({ children, sx = {}, ...props }) {
  return (
    <Paper variant="outlined" sx={{ p: 3, ...sx }} {...props}>
      {children}
    </Paper>
  );
}

