import { render, screen, fireEvent } from '@testing-library/react'
import { vi } from 'vitest'
import SlotPicker from '../src/pages/SlotPicker'

const mockClient = {
  getSlots: vi.fn(({ dateFrom, packageCode }) =>
    Promise.resolve([
      { id: 1, slot_date: dateFrom, start_time: '09:00', remaining: 2 },
      { id: 2, slot_date: dateFrom, start_time: '10:00', remaining: 1 },
    ])
  ),
}

test('SlotPicker loads slots and updates when package changes', async () => {
  render(<SlotPicker client={mockClient} />)

  // initial load
  expect(await screen.findByText(/09:00/)).toBeInTheDocument()

  // change package
  fireEvent.change(screen.getByLabelText(/แพ็กเกจ/), { target: { value: 'PREM' } })

  expect(mockClient.getSlots).toHaveBeenCalled()
})
