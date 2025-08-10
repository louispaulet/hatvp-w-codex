import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#facc15'];

function GenderDistribution() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/gender_counts.csv', d => ({
      gender: d.gender,
      count: +d.count,
    })).then(setData);
  }, []);

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Gender Distribution
      </Typography>
      <Typography variant="body1" color="text.secondary">
        Gender identities among declarants.
      </Typography>
      <Paper sx={{ mt: 3, height: 420, display: 'flex' }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie data={data} dataKey="count" nameKey="gender" outerRadius={120} label>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </Paper>
    </Container>
  );
}

export default GenderDistribution;
