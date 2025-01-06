import { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function RegisterPage() {
  const { signup } = useContext(UserContext)
  const navigate = useNavigate()

  const [user, setUser] = useState({
    name: "",
    email: "",
    password: "",
    confirmed_password: "",
  });
  const [passwordsMatch, setPasswordsMatch] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setPasswordsMatch(user.password === user.confirmed_password || user.confirmed_password.length === 0);
  }, [user.password, user.confirmed_password]);

  function onHandleChange(e) {
    const { id, value } = e.target;
    setUser((prevUser) => ({
      ...prevUser,
      [id]: value,
    }));
  }

  async function onHandleSubmit(e) {
    e.preventDefault();
    if (passwordsMatch && user.password === user.confirmed_password) {
  
      try {
        const data = await signup(user);
        if (data.status === 200) {
          console.log(data)
          navigate("/login");
        }
      } catch (error) {
        if (error.response && error.response.data)
        setError(error.response.data.error);
      }
    } else {
      setError("Passwords do not match.");
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-light-pink-orange">
      <div className="p-14 bg-white rounded-lg shadow-xl space-y-6 max-w-2xl w-full mx-4">
        <label
          htmlFor="name"
          className="block text-sm font-semibold text-words-pink-orange"
        >
          Enter your user name
        </label>
        <input
          id="name"
          type="text"
          placeholder="Enter your name"
          className="border-2 border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500"
          value={user.name}
          onChange={onHandleChange}
        />
        <label
          htmlFor="email"
          className="block text-sm font-semibold text-words-pink-orange"
        >
          Enter your email
        </label>
        <input
          id="email"
          type="email"
          placeholder="example@mail.com"
          className="border-2 border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500"
          value={user.email}
          onChange={onHandleChange}
        />
        <label
          htmlFor="password"
          className="block text-sm font-semibold text-words-pink-orange"
        >
          Enter your password
        </label>
        <input
          id="password"
          type="password"
          placeholder="password"
          className="border-2 border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500"
          value={user.password}
          onChange={onHandleChange}
        />
        <label
          htmlFor="confirmed_password"
          className="block text-sm font-semibold text-words-pink-orange"
        >
          Confirm your password
        </label>
        <input
          id="confirmed_password"
          type="password"
          placeholder="confirm password"
          className={`border-2 ${!passwordsMatch && user.confirmed_password.length > 0 ? "border-red-700" : "border-light-pink-orange"} bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500`}
          value={user.confirmed_password}
          onChange={onHandleChange}
        />
        {(!passwordsMatch && user.confirmed_password.length > 0) && <p className="text-red-700">Passwords must match</p>}
        {error && <p className="text-red-700">{error}</p>}
        <button
          type="submit"
          className="bg-pink-orange hover:bg-dark-pink-orange text-white font-bold py-2 px-4 rounded-lg w-full"
          onClick={onHandleSubmit}
        >
          Register
        </button>
        <div className="text-center text-gray-500">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-blue-500 hover:text-blue-700"
          >
            Login in here
          </Link>
        </div>
      </div>
    </div>
  );
}
