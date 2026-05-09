"""Tests für app.wiki_tools – ohne Modell-Calls, rein lokal."""

from __future__ import annotations

from pathlib import Path

import pytest

from app import wiki_tools


REPO_WIKI = Path(__file__).resolve().parents[2] / "wiki"


def test_load_index_contains_known_section():
    text = wiki_tools.load_index(wiki_root=REPO_WIKI)
    assert "Inhaltsverzeichnis" in text or "Übersicht" in text


def test_search_wiki_finds_b1_2():
    hits = wiki_tools.search_wiki("B1.2", max_results=5, wiki_root=REPO_WIKI)
    assert hits, "Suche nach B1.2 darf nicht leer sein"
    # Snippet darf nicht riesig sein
    for h in hits:
        assert len(h.snippet) <= 200


def test_search_wiki_empty_query_returns_empty():
    assert wiki_tools.search_wiki("   ", wiki_root=REPO_WIKI) == []


def test_read_page_works_for_index():
    content = wiki_tools.read_page("index", wiki_root=REPO_WIKI)
    assert "FAKT" in content


def test_read_page_rejects_traversal():
    with pytest.raises(wiki_tools.WikiPathError):
        wiki_tools.read_page("../CLAUDE", wiki_root=REPO_WIKI)


def test_read_page_rejects_absolute_path():
    with pytest.raises(wiki_tools.WikiPathError):
        wiki_tools.read_page("/etc/passwd", wiki_root=REPO_WIKI)


def test_read_page_missing_raises_filenotfound():
    with pytest.raises(FileNotFoundError) as exc:
        wiki_tools.read_page("massnahmen/Z99_existiert_nicht", wiki_root=REPO_WIKI)
    # Fehlermeldung sollte Kandidaten enthalten, damit das Modell sich
    # selbst korrigieren kann.
    assert "Ähnliche Slugs" in str(exc.value) or "list_pages" in str(exc.value)


def test_read_page_fuzzy_resolves_basename():
    """Slug ohne Verzeichnis (Wikilink-Stil) muss aufgelöst werden."""
    content = wiki_tools.read_page("E7_Bluehflaechen", wiki_root=REPO_WIKI)
    assert "E7" in content
    assert "Konditionalität" in content


def test_read_page_ambiguous_slug_lists_candidates():
    """Wenn mehrere Dateien matchen, müssen wir das deutlich machen."""
    # 'D2' kommt in mehreren Dateien vor — aber als Basename gibt's nur eine
    # eindeutige Datei pro Suffix. Wir testen mit einem konstruierten Fall:
    # 'A_Umweltbewusstes_Betriebsmanagement' existiert genau einmal, also
    # eindeutig. Wir prüfen den Mehrdeutigkeitspfad nur strukturell:
    err = wiki_tools.WikiAmbiguousSlugError("X", ["a/X", "b/X"])
    assert "mehrdeutig" in str(err)
    assert "a/X" in str(err)


def test_list_pages_with_prefix():
    pages = wiki_tools.list_pages(prefix="massnahmen/", wiki_root=REPO_WIKI)
    assert pages, "Erwartet mindestens eine Maßnahmen-Seite"
    assert all(p.startswith("massnahmen/") for p in pages)


def test_search_wiki_per_file_cap():
    """Eine einzelne Tabellenseite darf das Trefferbudget nicht aufbrauchen."""
    # 'E7' kommt sehr oft in Nutzcodeliste vor; wir wollen aber, dass auch
    # andere Dateien (insb. E7_Bluehflaechen.md) im Ergebnis auftauchen.
    hits = wiki_tools.search_wiki("E7", max_results=12, wiki_root=REPO_WIKI)
    distinct_pages = {h.page for h in hits}
    assert len(distinct_pages) >= 3, (
        f"Suche zu konzentriert auf wenige Seiten: {distinct_pages}"
    )


def test_build_directory_overview_lists_known_dirs():
    overview = wiki_tools.build_directory_overview(wiki_root=REPO_WIKI)
    assert "massnahmen/" in overview
    assert "Konzepte/" in overview
    assert "Antragstellung/" in overview
