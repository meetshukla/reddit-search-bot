import React, { useState } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from './components/ui/card';
import { Label } from './components/ui/label';
import { Input } from './components/ui/input';
import { Textarea } from './components/ui/textarea';
import { Button } from './components/ui/button';
import { Loader2 } from 'lucide-react';

function App() {
  const [subreddit, setSubreddit] = useState('');
  const [query, setQuery] = useState('');
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await axios.post('http://localhost:5000/search', {
        subreddit,
        query,
        prompt,
      });

      setResponse(result.data.response_text);
    } catch (error) {
      console.error(error);
      setResponse('An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>Reddit Search Agent</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="subreddit">Subreddit</Label>
              <Input
                id="subreddit"
                type="text"
                value={subreddit}
                onChange={(e) => setSubreddit(e.target.value)}
                placeholder="e.g., python"
                required
              />
            </div>
            <div>
              <Label htmlFor="query">Search Query</Label>
              <Input
                id="query"
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., web scraping"
                required
              />
            </div>
            <div>
              <Label htmlFor="prompt">Prompt</Label>
              <Textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Summarize the key points."
                required
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </form>
        </CardContent>
        {loading ? (
          <CardFooter>
            <div className="mt-6 flex justify-center">
              <Loader2 className="animate-spin" size={32} />
            </div>
          </CardFooter>
        ) : (
          response && (
            <CardFooter>
              <div className="mt-6">
                <h2 className="text-xl font-semibold mb-2">Response</h2>
                <div className="whitespace-pre-wrap break-words overflow-auto max-h-96 w-full p-4 border border-rounded-lg w-[452px]">
                  {response.split('\n').map((line, index) => {
                    const urlRegex = /(https?:\/\/[^\s]+)/g;
                    const parts = line.split(urlRegex);
                    return (
                      <div key={index}>
                        {parts.map((part, i) =>
                          urlRegex.test(part) ? (
                            <a
                              key={i}
                              href={part}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-500 underline"
                            >
                              Link
                            </a>
                          ) : (
                            part
                          )
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </CardFooter>
          )
        )}
      </Card>
    </div>
  );
}

export default App;
