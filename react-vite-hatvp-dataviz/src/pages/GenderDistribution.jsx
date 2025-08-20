import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';
import Typography from '@mui/material/Typography';
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
    </PageContainer>
  );
}

export default GenderDistribution;
