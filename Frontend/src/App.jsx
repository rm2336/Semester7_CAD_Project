import { useState, useEffect } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [count, setCount] = useState(0)
  useEffect(() => {
    fetch(`${API_URL}/recipes/`)
        .then(r => r.json())
        .then(data => console.log("Backend: ", data))
        .catch(err => console.error(err))
  }, [])

  return (
    <>
      <section id="center">
        <div>
          <h1>Food Recipes</h1>
          <p>
            Register to get started.
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => setCount((count) => count + 1)}
        >
        </button>
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
        <div id="social">
        </div>
      </section>

      <div className="ticks"></div>
      <section id="spacer"></section>
    </>
  )
}

export default App
