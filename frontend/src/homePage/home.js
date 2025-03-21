import React from 'react'
import PropTypes from 'prop-types'
import { useNavigate } from 'react-router-dom'
import Button from '@mui/material/Button'

const HomePage = (props) => {
  const { is_logged } = props
  const navigate = useNavigate()

  const on_button_click = () => {
    navigate('/login')
  }

  return (
    <div className='flex flex-col h-screen justify-center items-center m-auto'>
      <p className='mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl'>Welcome to Depex!</p>
      <p className='mb-6 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400 text-center'>
        Depex is a tool that allows you to reason over the entire version configuration space of the requirements files of an open-source
        software repository.
      </p>
      <div className='embed-responsive aspect-video'>
        <iframe
          className='embed-responsive-item rounded-lg'
          width='853'
          height='480'
          src='https://www.youtube.com/embed/8FoVLfNcx8o'
          allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
          allowFullScreen
        />
      </div>
      {is_logged ? null : (
        <div className='py-2'>
          <Button variant="contained" onClick={on_button_click}>Log In</Button>
        </div>
      )}
    </div>
  )
}

HomePage.propTypes = {
  is_logged: PropTypes.bool
}

export { HomePage }
