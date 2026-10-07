import { useEffect, useState } from 'react'
import { api } from '../api/client'

// รองรับ: FR-BKG-01, FR-BKG-06
export default function SlotPicker({ client = api, onSelect }) {
  const [packageCode, setPackageCode] = useState('STD')
  const [dateFrom, setDateFrom] = useState(new Date().toISOString().slice(0, 10))
  const [slots, setSlots] = useState([])

  useEffect(() => {
    let mounted = true
    client.getSlots({ dateFrom, packageCode }).then(data => {
      if (mounted) setSlots(data || [])
    })
    return () => (mounted = false)
  }, [dateFrom, packageCode, client])

  return (
    <div>
      <label>
        แพ็กเกจ:
        <select value={packageCode} onChange={e => setPackageCode(e.target.value)}>
          <option value="STD">STD</option>
          <option value="PREM">PREM</option>
        </select>
      </label>
      <label>
        เริ่มจากวันที่:
        <input type="date" value={dateFrom} onChange={e => setDateFrom(e.target.value)} />
      </label>
      <ul>
        {slots.map(s => (
          <li key={s.id}>
            {s.slot_date} {s.start_time} — เหลือ {s.remaining}
            <button onClick={() => onSelect && onSelect(s)}>เลือก</button>
          </li>
        ))}
      </ul>
    </div>
  )
}
