import { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext";

export default function LoginPage() {
  const { login } = useContext(UserContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const onHandleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await login(email, password);
      if (response.status == 200) {
        navigate('/files');
      }
    } catch (error) {
      if (error.response && error.response.data){
        console.log(error.response.data)
        setError(error.response.data.message);
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-light-pink-orange">
      <div className="p-14 bg-white rounded-lg shadow-xl space-y-6 max-w-2xl w-full mx-4">
        <label
          htmlFor="email"
          className="block text-sm font-semibold text-words-pink-orange"
        >
          Enter your email
        </label>
        <input
          id="email"
          type="email"
          placeholder="Your Email"
          className="border-2 border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500"
          onChange={(event) => setEmail(event.target.value)}
          value={email}
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
          placeholder="Your Password"
          className="border-2 border-light-pink-orange bg-gray-50 h-10 px-5 rounded-lg text-sm focus:outline-none w-full placeholder-gray-500"
          onChange={(event) => setPassword(event.target.value)}
          value={password}
        />
        <div className="text-right">
          <label className="text-blue-500 hover:text-blue-700">
            <Link
              to="/forgotpassword"
              className="text-blue-500 hover:text-blue-700"
            >
              Forgot password?
            </Link>
          </label>
        </div>
        {error && <p className="text-red-700">{error}</p>}
        <form onSubmit={onHandleSubmit}>
          <button
            type="submit"
            className="bg-pink-orange hover:bg-dark-pink-orange text-white font-bold py-2 px-4 rounded-lg w-full"
          >
            Log In
          </button>
        </form>
        <div className="text-center text-gray-500">
          Don't have an account yet?{" "}
          <Link to="/signup" className="text-blue-500 hover:text-blue-700">
            Sign up here
          </Link>
        </div>
      </div>
    </div>
  );
}
