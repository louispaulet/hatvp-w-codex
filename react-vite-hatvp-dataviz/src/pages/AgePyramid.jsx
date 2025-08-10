import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import * as d3 from 'd3';

function AgePyramid() {
  const [data, setData] = useState([]);

  useEffect(() => {
    d3.csv('/age_pyramid.csv', d => ({
      age_band: d.age_band,
      male: +d.male,
      female: +d.female,
    })).then(raw => {
      raw.sort((a, b) => {
        const ageA = parseInt(a.age_band.split('-')[0], 10);
        const ageB = parseInt(b.age_band.split('-')[0], 10);
        return ageB - ageA; // Oldest first
      });
      setData(raw);
    });
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Age Pyramid by Gender</h1>
      <p className="text-sm text-gray-600 mb-4">
        Age distribution split by gender.
      </p>
      <div className="h-[700px] max-w-md mx-auto md:mx-32 lg:mx-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" stackOffset="sign">
            <XAxis type="number" domain={['dataMin', 'dataMax']} />
            <YAxis dataKey="age_band" type="category" />
            <Tooltip formatter={(value) => Math.abs(value)} />
            <Bar dataKey="male" stackId="a" fill="#3b82f6" name="Male" />
            <Bar dataKey="female" stackId="a" fill="#ef4444" name="Female" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default AgePyramid;
