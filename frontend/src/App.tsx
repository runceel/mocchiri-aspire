import { useEffect, useState } from 'react'

type Book = {
  id: number
  title: string
  price: number
  stock: number
  sold: number
}

type RankingItem = {
  id: number
  title: string
  sold: number
}

type Dashboard = {
  books: Book[]
  ranking: RankingItem[]
}

const yen = new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' })

async function fetchDashboard(): Promise<Dashboard> {
  const [booksRes, rankingRes] = await Promise.all([fetch('/api/books'), fetch('/api/ranking')])
  if (!booksRes.ok || !rankingRes.ok) {
    throw new Error('API の呼び出しに失敗しました')
  }
  return { books: await booksRes.json(), ranking: await rankingRes.json() }
}

function App() {
  const [{ books, ranking }, setDashboard] = useState<Dashboard>({ books: [], ranking: [] })
  const [error, setError] = useState<string | null>(null)
  const [version, setVersion] = useState(0)

  useEffect(() => {
    fetchDashboard()
      .then((dashboard) => {
        setDashboard(dashboard)
        setError(null)
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
  }, [version])

  const sell = async (book: Book) => {
    const res = await fetch(`/api/books/${book.id}/sales`, { method: 'POST' })
    if (!res.ok) {
      const body = await res.json().catch(() => null)
      setError(body?.detail ?? `頒布に失敗しました (${res.status})`)
      return
    }
    // 頒布したら読み込み直す
    setVersion((v) => v + 1)
  }

  return (
    <div className="app">
      <header>
        <h1>もっちり頒布マネージャー</h1>
        <p>技術書典 もっちりソフトのブース用</p>
      </header>

      {error && <p className="error">{error}</p>}

      <main>
        <section className="books">
          <h2>頒布状況</h2>
          <table>
            <thead>
              <tr>
                <th>タイトル</th>
                <th className="num">価格</th>
                <th className="num">在庫</th>
                <th className="num">頒布数</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {books.map((book) => (
                <tr key={book.id}>
                  <td>{book.title}</td>
                  <td className="num">{yen.format(book.price)}</td>
                  <td className="num">{book.stock}</td>
                  <td className="num">{book.sold}</td>
                  <td>
                    <button onClick={() => sell(book)} disabled={book.stock <= 0}>
                      頒布する
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="ranking">
          <h2>売れ行きランキング</h2>
          <ol>
            {ranking.map((item) => (
              <li key={item.id}>
                <span className="title">{item.title}</span>
                <span className="sold">{item.sold} 冊</span>
              </li>
            ))}
          </ol>
          <p className="note">ランキングは 30 秒キャッシュしています</p>
        </section>
      </main>
    </div>
  )
}

export default App
