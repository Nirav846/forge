import React from 'react';
import { render, waitFor, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ComplexesLibrary from './components/complexes/ComplexesLibrary';
import realData from './data/complexes.json';

describe('ComplexesLibrary crash repro', () => {
  it('renders cards + modal without throwing #310', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    globalThis.fetch = vi.fn(async () => ({ ok: true, json: async () => JSON.parse(JSON.stringify(realData)) })) as any;
    const { container } = render(<ComplexesLibrary />);
    await new Promise(r => setTimeout(r, 50));
    await waitFor(() => {
      expect(container.textContent).toContain('Pace Bowler - Preparation Complex');
    });
    const btns = Array.from(container.querySelectorAll('button')).filter(b => b.textContent?.includes('View Protocol'));
    fireEvent.click(btns[0]);
    await waitFor(() => {
      expect(container.textContent).toContain('Coaching Notes');
    });
    const errors = spy.mock.calls.filter(c => String(c[0]).includes('Objects are not valid') || String(c[0]).includes('310'));
    console.log('OBJECT RENDER ERRORS:', errors.length);
    if (errors.length) console.log(errors[0].map(String).join('\n').slice(0, 800));
    spy.mockRestore();
  });
});
