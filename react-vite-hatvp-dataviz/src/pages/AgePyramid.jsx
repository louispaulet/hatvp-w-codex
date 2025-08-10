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
    })).then(setData);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold">Age Pyramid by Gender</h1>
      <p className="text-sm text-gray-600 mb-4">
        Age distribution split by gender.
      </p>
      <div className="w-full h-96">
        <ResponsiveContainer>
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
