import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import InsightsIcon from '@mui/icons-material/Insights';
import { PageContainer, SectionCard } from '../components/Layout';
import SectionTitle from '../components/SectionTitle';

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
    <PageContainer>
      <SectionTitle icon={<InsightsIcon color="primary" />} title="Gender Distribution" subtitle="Gender identities among declarants." />
      <SectionCard sx={{ mt: 2, height: 420, display: 'flex' }}>
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
      </SectionCard>
      <SectionCard sx={{ mt: 2 }}>
        <SectionTitle icon={<InsightsIcon color="primary" />} title="About this chart" />
        <div style={{ marginTop: 8 }}>
          <Typography variant="body1" sx={{ mb: 1 }}>
            This pie chart summarizes the <strong>gender split among declarants</strong> (HATVP declarations).
          </Typography>
          <Typography variant="subtitle2" sx={{ mt: 1 }}>Breakdown</Typography>
          <ul style={{ marginTop: 4, marginBottom: 8 }}>
            <li>
              <Typography variant="body2">
                <strong>Blue (men)</strong>: <strong>7,692 declarants</strong>
              </Typography>
            </li>
            <li>
              <Typography variant="body2">
                <strong>Red (women)</strong>: <strong>4,298 declarants</strong>
              </Typography>
            </li>
          </ul>
          <Divider sx={{ my: 1.5 }} />
          <Typography variant="subtitle2">Key takeaways</Typography>
          <ul style={{ marginTop: 4 }}>
            <li>
              <Typography variant="body2">Men make up <strong>~64%</strong> of declarants.</Typography>
            </li>
            <li>
              <Typography variant="body2">Women account for only <strong>~36%</strong>.</Typography>
            </li>
            <li>
              <Typography variant="body2">This confirms the imbalance we saw in the age pyramid: <strong>men are nearly twice as represented as women</strong>.</Typography>
            </li>
          </ul>
          <Typography variant="body2" sx={{ mt: 1 }}>
            👉 In other words, for every woman declarant, there are about <strong>1.8 men</strong>.
          </Typography>
          <Typography variant="body2" sx={{ mt: 1.5 }}>
            Would you like me to combine the three plots (age distribution, pyramid, and pie chart) into a short <strong>narrative analysis</strong> that could work in a report?
          </Typography>
        </div>
      </SectionCard>
    </PageContainer>
  );
}

export default GenderDistribution;
