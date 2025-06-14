import React from 'react';

const YoutubeLogo = () => {
  return (
    <div className="absolute top-2 right-11 mr-11 w-[150px] h-[120px]">
      {/* YouTube Logo */}
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="150"
        height="100"
        viewBox="0 0 256 180"
        className="absolute top-0 left-0"
      >
        <path
          fill="#f00"
          d="M250.346 28.075A32.18 32.18 0 0 0 227.69 5.418C207.824 0 127.87 0 127.87 0S47.912.164 28.046 5.582A32.18 32.18 0 0 0 5.39 28.24c-6.009 35.298-8.34 89.084.165 122.97a32.18 32.18 0 0 0 22.656 22.657c19.866 5.418 99.822 5.418 99.822 5.418s79.955 0 99.82-5.418a32.18 32.18 0 0 0 22.657-22.657c6.338-35.348 8.291-89.1-.164-123.134"
        />
        <path
          fill="#fff"
          d="m102.421 128.06l66.328-38.418l-66.328-38.418z"
        />
      </svg>

      {/* X Overlay */}
      <div className="absolute inset-0 pointer-events-none top-0 -mt-2">
        <div className="absolute w-[8px] h-full bg-black rotate-45 left-1/2 top-0 -translate-x-1/2" />
        <div className="absolute w-[8px] h-full bg-black -rotate-45 left-1/2 top-0 -translate-x-1/2" />
      </div>
    </div>
  );
};

export default YoutubeLogo;
