import React, { useState, useEffect } from 'react'
import { RouterProvider, createBrowserRouter, Outlet } from 'react-router-dom'
import { Home, Boxes, CircleHelp } from 'lucide-react'
import { HomePage } from '../homePage/home'
import { HelpPage } from '../helpPage/help'
import { LoginPage } from '../auth/login'
import { SignUpPage } from '../auth/signup'
import { ProtectedRoute } from '../auth/protectedRoute'
import { RepositoriesPage } from '../repositoriesPage/repositories'
import Sidebar, { SidebarItem } from '../components/sidebar'

function Routes() {
  const access_token = useState(localStorage.getItem('access_token'))[0]
  const [is_logged, set_is_logged] = useState(false)

  useEffect(() => {
    fetch('http://localhost:8000/user/verify_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ access_token })
    })
      .then((r) => r.json())
      .then((r) => {
        if (r.valid) {
          set_is_logged(true)
        } else {
          localStorage.removeItem('access_token')
          set_is_logged(false)
        }
      })
  }, [])

  const SidebarLayout = () => (
    <>
      <Sidebar is_logged={is_logged}>
        <SidebarItem icon={<Home size={20} />} text='Home' route='/' />
        {is_logged ? <SidebarItem icon={<Boxes size={20} />} text='Repositories' route='/repositories' /> : null}
        <SidebarItem icon={<CircleHelp size={20} />} text='Help' route='/help' />
      </Sidebar>
      <Outlet />
    </>
  )

  const routesForSidebar = [
    {
      path: '/',
      element: <HomePage is_logged={is_logged} />
    },
    {
      path: '/login',
      element: <LoginPage />
    },
    {
      path: '/signup',
      element: <SignUpPage />
    },
    {
      path: '/help',
      element: <HelpPage />
    },
    {
      path: '/',
      element: <ProtectedRoute />,
      children: [
        {
          path: '/repositories',
          element: <RepositoriesPage />
        }
      ]
    }
  ]

  const routesForPublic = [
    {
      path: '/',
      element: <HomePage is_logged={is_logged} />
    },
    {
      path: '/login',
      element: <LoginPage />
    },
    {
      path: '/signup',
      element: <SignUpPage />
    },
    {
      path: '/help',
      element: <HelpPage />
    }
  ]

  const routesForAuthenticatedOnly = [
    {
      path: '/',
      element: <ProtectedRoute />,
      children: [
        {
          path: '/repositories',
          element: <RepositoriesPage />
        }
      ]
    }
  ]

  const router = createBrowserRouter([
    {
      element: <SidebarLayout />,
      children: [...routesForSidebar]
    },
    ...routesForPublic,
    ...routesForAuthenticatedOnly
  ])

  return <RouterProvider router={router} />
}

export default Routes