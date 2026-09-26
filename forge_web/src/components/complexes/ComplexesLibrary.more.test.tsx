import { render, waitFor, fireEvent, cleanup } from '@testing-library/react';
import { describe, it, expect, vi, afterEach } from 'vitest';
import ComplexesLibrary from './ComplexesLibrary';
import publicData from '../../../../../public/data/complexes.json';

const clone = () => JSON.parse(JSON.stringify(publicData));

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('click +X more exercises', () => {
  it('expands the full exercise list inline without crashing (blank-page repro)', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const data = clone();
    (data as any[]).sort((a: any, b: any) => (b.exercises?.length ?? 0) - (a.exercises?.length ?? 0));
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => data })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercises'));

    const btns = Array.from(container.querySelectorAll('button')).filter(b => b.textContent?.includes('more exercises'));
    expect(btns.length).toBeGreaterThan(0);
    const card = btns[0].closest('.bg-white') as HTMLElement;
    // collapsed: only 3 numbered rows visible in this card
    expect(card.querySelectorAll('.space-y-2 > div').length).toBe(3);

    fireEvent.click(btns[0]);
    await new Promise(r => setTimeout(r, 30));

    // expanded: all exercises of that complex are now listed
    const target = (data as any[]).find(c => c.name === card.querySelector('h3')?.textContent);
    expect(target).toBeTruthy();
    expect(card.querySelectorAll('.space-y-2 > div').length).toBe(target!.exercises.length);
    expect(card.textContent).toContain('Show less');
    // page is NOT blank
    expect((container.textContent ?? '').length).toBeGreaterThan(500);
    const errs = spy.mock.calls.filter(c => String(c[0]).includes('Minified') || String(c[0]).includes('Objects are not valid') || String(c[0]).includes('Cannot read'));
    expect(errs).toEqual([]);

    // collapse again
    fireEvent.click(Array.from(card.querySelectorAll('button')).find(b => b.textContent?.includes('Show less'))!);
    await new Promise(r => setTimeout(r, 30));
    expect(card.querySelectorAll('.space-y-2 > div').length).toBe(3);
  });

  it('survives malformed records (null exercises / missing fields) without blanking', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const data = clone() as any[];
    data[0].exercises = null;
    delete data[1].equipment;
    data[2].exercises = [null, { sets: 3 }];
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => data })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercises'));
    expect((container.textContent ?? '').length).toBeGreaterThan(500);
    const btns = Array.from(container.querySelectorAll('button')).filter(b => b.textContent?.includes('more exercises'));
    if (btns.length) { fireEvent.click(btns[0]); await new Promise(r => setTimeout(r, 30)); }
    expect(spy.mock.calls.filter(c => String(c[0]).includes('Minified'))).toEqual([]);
  });

  it('detail modal still opens via View Protocol and shows all exercises', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const data = clone();
    (data as any[]).sort((a: any, b: any) => (b.exercises?.length ?? 0) - (a.exercises?.length ?? 0));
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => data })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercises'));
    const viewBtns = Array.from(container.querySelectorAll('button')).filter(b => b.textContent?.includes('View Protocol'));
    fireEvent.click(viewBtns[0]);
    await waitFor(() => expect(container.textContent).toContain('Coaching Notes'));
    expect(container.textContent).toContain('Protocol');
    expect(spy.mock.calls.filter(c => String(c[0]).includes('Minified'))).toEqual([]);
  });
});
