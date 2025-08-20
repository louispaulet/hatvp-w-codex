import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

function SectionTitle({ icon, title, subtitle }) {
  return (
    <Stack spacing={subtitle ? 0.5 : 0} sx={{ mb: 1 }}>
      <Stack direction="row" spacing={1} alignItems="center">
        {icon}
        <Typography variant="h5" component="h2" sx={{ fontWeight: 700 }}>
          {title}
        </Typography>
      </Stack>
      {subtitle ? (
        <Typography variant="body2" color="text.secondary">{subtitle}</Typography>
      ) : null}
    </Stack>
  );
}

export default SectionTitle;
