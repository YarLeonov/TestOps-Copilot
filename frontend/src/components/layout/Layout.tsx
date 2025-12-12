import { Link, NavLink } from "react-router-dom";
import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

function Layout({ children }: LayoutProps) {
  return (
    <div className="app-root">
      <header className="app-header">
        <Link to="/" className="app-logo">
          TestOps Copilot
        </Link>
        <nav className="app-nav">
          <NavLink
            to="/ui"
            className={({ isActive }) =>
              "app-nav-link" + (isActive ? " app-nav-link-active" : "")
            }
          >
            UI сценарий
          </NavLink>
          <NavLink
            to="/api"
            className={({ isActive }) =>
              "app-nav-link" + (isActive ? " app-nav-link-active" : "")
            }
          >
            API сценарий
          </NavLink>
        </nav>
      </header>

      <main className="app-main">{children}</main>

      <footer className="app-footer">
        <span>AI помощник для TestOps на хакатоне</span>
      </footer>
    </div>
  );
}

export default Layout;
