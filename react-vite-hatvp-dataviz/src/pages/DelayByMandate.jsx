import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

function DelayByMandate() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/mandate_delay_median.csv', d => ({
      mandate_type: d.mandate_type,
      delay_days: +d.delay_days,
    })).then(setData);
  }, []);

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Median Publication Delay by Mandate
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Median days between deposit and publication.
      </Typography>
      <Paper sx={{ mt: 3, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="mandate_type" angle={-45} textAnchor="end" height={120} />
            <YAxis />
            <Tooltip />
            <Bar dataKey="delay_days" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>
    </Container>
  );
}

export default DelayByMandate;
