/**
 * Regression tests for the "View Protocol" button.
 *
 * Bug: clicking "View Protocol" could leave the page blank because the
 * dataset contained duplicate complex ids (React key collisions made two
 * cards reconcile as one), and the modal rendered nested fields without any
 * defensive guards so a single malformed record crashed the whole tree.
 */
import { render, waitFor, fireEvent, cleanup } from '@testing-library/react';
import { describe, it, expect, vi, afterEach } from 'vitest';
import ComplexesLibrary from './ComplexesLibrary';
import publicData from '../../../public/data/complexes.json';

const clone = () => JSON.parse(JSON.stringify(publicData));

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('View Protocol button', () => {
  it('opens the detail modal for every card with the real dataset (no key collisions)', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => clone() })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercise Complexes'));

    // Dataset must not contain duplicate ids anymore
    const ids = (publicData as any[]).map(c => c.id);
    expect(new Set(ids).size).toBe(ids.length);

    const viewBtns = Array.from(container.querySelectorAll('button'))
      .filter(b => b.textContent?.includes('View Protocol'));
    expect(viewBtns.length).toBeGreaterThan(0);

    // Open the modal for several cards (including previously-colliding ones)
    for (const btn of [viewBtns[0], viewBtns[Math.floor(viewBtns.length / 2)], viewBtns[viewBtns.length - 1]]) {
      fireEvent.click(btn);
      await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeTruthy());
      expect(container.textContent).toContain('Protocol');
      expect(container.textContent).toContain('Coaching Notes');
      expect(container.textContent).toContain('Equipment Needed');
      // Close via X button
      const dialog = container.querySelector('[role="dialog"]') as HTMLElement;
      fireEvent.click(dialog.querySelector('button')!);
      await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeNull());
    }

    // Page is not blank and no React crash was logged
    expect((container.textContent ?? '').length).toBeGreaterThan(500);
    expect(spy.mock.calls.filter(c => String(c[0]).includes('Minified') || String(c[0]).includes('Objects are not valid'))).toEqual([]);
  });

  it('closes the modal with Escape', async () => {
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => clone() })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercise Complexes'));
    const viewBtns = Array.from(container.querySelectorAll('button'))
      .filter(b => b.textContent?.includes('View Protocol'));
    fireEvent.click(viewBtns[0]);
    await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeTruthy());
    fireEvent.keyDown(window, { key: 'Escape' });
    await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeNull());
  });

  it('survives duplicate ids and malformed records without blanking', async () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const data = clone() as any[];
    // Re-introduce an id collision + malformed entries to prove defensiveness
    data[1].id = data[0].id;
    data[2].exercises = null;
    delete data[3].equipment;
    data[4].exercises = [null, { sets: 3 }];
    (globalThis as any).fetch = vi.fn(async () => ({ ok: true, json: async () => data })) as any;
    const { container } = render(<ComplexesLibrary />);
    await waitFor(() => expect(container.textContent).toContain('Exercise Complexes'));

    const viewBtns = Array.from(container.querySelectorAll('button'))
      .filter(b => b.textContent?.includes('View Protocol'));
    // Every colliding/malformed card still renders its own button
    expect(viewBtns.length).toBe(data.length);

    for (const btn of viewBtns.slice(0, 6)) {
      fireEvent.click(btn);
      await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeTruthy());
      expect((container.textContent ?? '').length).toBeGreaterThan(500);
      const dialog = container.querySelector('[role="dialog"]') as HTMLElement;
      // Close via overlay click
      fireEvent.click(dialog.firstElementChild!.firstElementChild!);
      await waitFor(() => expect(container.querySelector('[role="dialog"]')).toBeNull());
    }
    expect(spy.mock.calls.filter(c => String(c[0]).includes('Minified') || String(c[0]).includes('Objects are not valid'))).toEqual([]);
  });
});
