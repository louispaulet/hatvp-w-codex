import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

function AgeDistribution() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/age_band_counts.csv', d => ({
      age_band: d.age_band,
      count: +d.count,
    })).then(setData);
  }, []);

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Declarant Age Distribution
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Age bands among declarants.
      </Typography>
      <Paper sx={{ mt: 3, height: 420 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="age_band" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#1976d2" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>
    </Container>
  );
}

export default AgeDistribution;
